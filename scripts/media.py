#!/usr/bin/env python3
"""Media tier: image, voice and avatar-video generation. Reads the "media"
block of ops/model-routing.json. Cheap OpenRouter models by default,
HeyGen for voice clones and talking-avatar video.

  python scripts/media.py image "a flat logo of a fox"          [--out file.png]
  python scripts/media.py voice "Hello from Karvelta"            [--engine heygen] [--voice ID]
  python scripts/media.py video "a drone shot over Manchester at dusk"  [--duration 8] [--aspect 9:16]
  python scripts/media.py talking "Script to speak" --photo face.png         (Avatar IV via OpenRouter)
  python scripts/media.py talking "Script to speak" --avatar ID --voice ID   (HeyGen direct, own avatars)
  python scripts/media.py voices   [--language English]   (HeyGen voice IDs)
  python scripts/media.py avatars                           (HeyGen avatar IDs)

Stdlib only. Files land in media-out/ (gitignored) unless --out is given.
The saved file path is printed to stdout; status goes to stderr."""
import argparse
import base64
import datetime
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROUTING_PATH = REPO_ROOT / "ops" / "model-routing.json"
ENV_PATH = REPO_ROOT / ".env"
OUT_DIR = REPO_ROOT / "media-out"
OPENROUTER = "https://openrouter.ai/api/v1"
HEYGEN = "https://api.heygen.com"


class EngineFailed(Exception):
    """One model/engine failed in a way the next one in the chain might not."""


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def log(msg: str) -> None:
    print(f"[media] {msg}", file=sys.stderr)


def need_key(name: str) -> str:
    key = os.environ.get(name, "").strip()
    if not key:
        raise EngineFailed(f"{name} is not set in .env")
    return key


def http_json(url: str, method: str = "GET", headers: dict = None, body: dict = None, timeout: int = 120) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Always fall through (even on 401/402): a voice job can still
        # succeed on HeyGen when OpenRouter has no credits.
        raise EngineFailed(f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise EngineFailed(f"network error: {e}")


def out_path(explicit: str, kind: str, ext: str) -> Path:
    if explicit:
        return Path(explicit)
    OUT_DIR.mkdir(exist_ok=True)
    return OUT_DIR / f"{kind}-{datetime.datetime.now():%Y%m%d-%H%M%S}.{ext}"


def download(url: str, dest: Path, headers: dict = None) -> None:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=300) as resp:
        dest.write_bytes(resp.read())


def run_chain(chain: list, fn, *args, nested: bool = False):
    """Try each engine/model in order; return the first success. A nested
    chain raises instead of exiting so the outer chain can fall through."""
    failures = []
    for item in chain:
        try:
            result = fn(item, *args)
            log(f"used: {item}")
            return result
        except EngineFailed as e:
            failures.append(f"  {item}: {e}")
            log(f"{item} failed, trying next")
    if nested:
        raise EngineFailed("all models failed")
    sys.exit("error: every option failed:\n" + "\n".join(failures))


# ---------- image (OpenRouter Images API) ----------

def image_openrouter(model: str, prompt: str, out: str) -> Path:
    key = need_key("OPENROUTER_API_KEY")
    data = http_json(f"{OPENROUTER}/images", "POST", {"Authorization": f"Bearer {key}"},
                     {"model": model, "prompt": prompt})
    try:
        item = data["data"][0]
    except (KeyError, IndexError, TypeError):
        raise EngineFailed(f"no image in response: {str(data)[:200]}")
    ext = item.get("media_type", "image/png").split("/")[-1]
    dest = out_path(out, "image", ext)
    dest.write_bytes(base64.b64decode(item["b64_json"]))
    return dest


# ---------- voice ----------

def pcm16_to_wav(pcm: bytes, rate: int = 24000) -> bytes:
    # OpenAI audio models stream raw 16-bit mono PCM at 24 kHz; wrap it in a WAV header.
    header = b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt " + struct.pack(
        "<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16) + b"data" + struct.pack("<I", len(pcm))
    return header + pcm


def voice_openrouter(model: str, text: str, voice: str, out: str) -> Path:
    key = need_key("OPENROUTER_API_KEY")
    body = {
        "model": model,
        "modalities": ["text", "audio"],
        "audio": {"voice": voice or "alloy", "format": "pcm16"},
        "stream": True,  # OpenRouter requires streaming for audio output
        "messages": [
            {"role": "system", "content": "Read the user's text aloud exactly as written. Add nothing."},
            {"role": "user", "content": text},
        ],
    }
    req = urllib.request.Request(f"{OPENROUTER}/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 method="POST", headers={"Content-Type": "application/json",
                                                         "Authorization": f"Bearer {key}"})
    chunks = []
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            for raw in resp:  # server-sent events, one "data: {...}" per line
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                try:
                    evt = json.loads(line[5:])
                except json.JSONDecodeError:
                    continue
                for choice in evt.get("choices", []):
                    b64 = (choice.get("delta", {}).get("audio") or {}).get("data")
                    if b64:
                        chunks.append(b64)
    except urllib.error.HTTPError as e:
        raise EngineFailed(f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
    except (urllib.error.URLError, TimeoutError) as e:
        raise EngineFailed(f"network error: {e}")
    if not chunks:
        raise EngineFailed("stream returned no audio")
    dest = out_path(out, "voice", "wav")
    dest.write_bytes(pcm16_to_wav(base64.b64decode("".join(chunks))))
    return dest


def voice_heygen(text: str, voice: str, out: str) -> Path:
    key = need_key("HEYGEN_API_KEY")
    if not voice:
        raise EngineFailed("HeyGen needs --voice (or media.voice.heygen_default_voice in the config); "
                           "list IDs with: python scripts/media.py voices")
    data = http_json(f"{HEYGEN}/v3/voices/speech", "POST", {"x-api-key": key},
                     {"text": text, "voice_id": voice})
    url = (data.get("data") or {}).get("audio_url")
    if not url:
        raise EngineFailed(f"no audio_url in response: {str(data)[:200]}")
    ext = Path(urllib.parse.urlparse(url).path).suffix.lstrip(".") or "mp3"
    dest = out_path(out, "voice", ext)
    download(url, dest)
    return dest


# ---------- text-to-video (OpenRouter Videos API: Veo etc.) ----------

def video_openrouter(model: str, prompt: str, opts: dict, out: str, wait: int) -> Path:
    """opts holds any Videos API body fields; None values are left out, since
    some models reject fields they don't support (e.g. Avatar IV: duration)."""
    key = need_key("OPENROUTER_API_KEY")
    auth = {"Authorization": f"Bearer {key}"}
    body = {"model": model, "prompt": prompt, **{k: v for k, v in opts.items() if v is not None}}
    job = http_json(f"{OPENROUTER}/videos", "POST", auth, body)
    job_id = job.get("id")
    if not job_id:
        raise EngineFailed(f"no job id: {str(job)[:200]}")
    log(f"{model} job {job_id} queued; polling every 15s (up to {wait}s)")
    deadline = time.time() + wait
    while time.time() < deadline:
        time.sleep(15)
        info = http_json(f"{OPENROUTER}/videos/{job_id}", headers=auth)
        status = info.get("status")
        log(f"status: {status}")
        if status == "completed":
            url = (info.get("unsigned_urls") or [None])[0]
            if not url:
                raise EngineFailed("completed but no video URL")
            dest = out_path(out, "video", "mp4")
            # Only send the OpenRouter key back to OpenRouter, never to a storage host.
            host = urllib.parse.urlparse(url).hostname or ""
            download(url, dest, auth if host.endswith("openrouter.ai") else None)
            return dest
        if status in ("failed", "cancelled", "expired"):
            raise EngineFailed(f"job {status}: {str(info)[:200]}")
    # Do not fall through to another model here: this job may still finish and bill.
    sys.exit(f"error: still rendering after {wait}s. Check later: GET {OPENROUTER}/videos/{job_id}")


def image_ref(photo: str) -> str:
    """A URL passes through; a local file becomes a base64 data URL."""
    if photo.startswith(("http://", "https://")):
        return photo
    path = Path(photo)
    if not path.exists():
        sys.exit(f"error: photo not found: {photo}")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(path.suffix.lower().lstrip("."), "png")
    return f"data:image/{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


# ---------- HeyGen avatar video (direct API, own avatars) ----------

def video_heygen(script: str, avatar: str, voice: str, out: str, wait: int) -> Path:
    key = need_key("HEYGEN_API_KEY")
    created = http_json(f"{HEYGEN}/v3/videos", "POST", {"x-api-key": key},
                        {"type": "avatar", "avatar_id": avatar, "script": script, "voice_id": voice})
    video_id = (created.get("data") or {}).get("video_id")
    if not video_id:
        sys.exit(f"error: HeyGen did not return a video_id: {str(created)[:300]}")
    log(f"video {video_id} queued; polling every 15s (up to {wait}s)")
    deadline = time.time() + wait
    while time.time() < deadline:
        time.sleep(15)
        info = http_json(f"{HEYGEN}/v3/videos/{video_id}", headers={"x-api-key": key})
        info = info.get("data", info)
        status = info.get("status")
        log(f"status: {status}")
        if status == "completed":
            dest = out_path(out, "video", "mp4")
            download(info["video_url"], dest)
            return dest
        if status == "failed":
            sys.exit(f"error: HeyGen video failed: {str(info)[:300]}")
    sys.exit(f"error: still rendering after {wait}s. Check later: GET {HEYGEN}/v3/videos/{video_id}")


def list_heygen(path: str, params: dict) -> None:
    key = need_key("HEYGEN_API_KEY")
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    data = http_json(f"{HEYGEN}{path}?{query}", headers={"x-api-key": key})
    for item in data.get("data") or []:
        ident = item.get("voice_id") or item.get("id")
        extra = item.get("language") or item.get("avatar_type") or ""
        print(f"{ident}\t{item.get('name', '')}\t{extra}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp1252 consoles crash on non-ASCII
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Image, voice and avatar-video generation (media tier).")
    p.add_argument("job", choices=["image", "voice", "video", "talking", "voices", "avatars"])
    p.add_argument("text", nargs="*", help="prompt (image/video), text to speak (voice) or script (talking)")
    p.add_argument("--out", help="output file path (default: media-out/<job>-<timestamp>.<ext>)")
    p.add_argument("--engine", choices=["openrouter", "heygen"], help="voice only: force one engine")
    p.add_argument("--voice", help="voice id/name (OpenRouter: alloy, nova...; HeyGen: voice_id)")
    p.add_argument("--photo", help="talking: photo file or URL to animate (OpenRouter Avatar IV)")
    p.add_argument("--avatar", help="talking: HeyGen avatar look id (HeyGen direct)")
    p.add_argument("--language", help="filter for 'voices'")
    p.add_argument("--duration", type=int, default=8, help="video: seconds (Veo supports 4, 6, 8)")
    p.add_argument("--resolution", default="720p", help="video: 720p (cheapest), 1080p, 4K")
    p.add_argument("--aspect", default="16:9", help="video: 16:9 or 9:16")
    p.add_argument("--no-audio", action="store_true", help="video: silent clip (cheaper)")
    p.add_argument("--wait", type=int, default=900, help="video/talking: max seconds to wait for render")
    args = p.parse_args()
    text = " ".join(args.text).strip()

    try:
        load_dotenv(ENV_PATH)
        cfg = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))["tiers"]["media"]

        if args.job == "voices":
            return list_heygen("/v3/voices", {"language": args.language, "limit": 100})
        if args.job == "avatars":
            return list_heygen("/v3/avatars/looks", {"limit": 50})
        if not text:
            sys.exit(f"error: '{args.job}' needs text")

        if args.job == "image":
            dest = run_chain(cfg["image"]["model"], image_openrouter, text, args.out)
        elif args.job == "voice":
            vcfg = cfg["voice"]
            order = [args.engine] if args.engine else vcfg["order"]

            def voice_engine(engine, text, out):
                if engine == "heygen":
                    return voice_heygen(text, args.voice or vcfg.get("heygen_default_voice", ""), out)
                return run_chain(vcfg["model"], voice_openrouter, text, args.voice, out, nested=True)

            dest = run_chain(order, voice_engine, text, args.out)
        elif args.job == "video":
            opts = {"duration": args.duration, "resolution": args.resolution,
                    "aspect_ratio": args.aspect, "generate_audio": not args.no_audio}
            dest = run_chain(cfg["video"]["model"], video_openrouter, text, opts, args.out, args.wait)
        elif args.photo:  # talking via OpenRouter (HeyGen Avatar IV): photo + script, no HeyGen key
            opts = {"resolution": args.resolution, "aspect_ratio": args.aspect,
                    # Avatar IV rejects frame_images; the photo goes in as a reference image.
                    "input_references": [{"type": "image_url", "image_url": {"url": image_ref(args.photo)}}]}
            # Avatar IV needs a HeyGen voice for a text script (stock voices work on the
            # OpenRouter key). Shape confirmed by the API's own error: provider.options.heygen.voice_id
            voice = args.voice or cfg["talking"].get("default_voice")
            opts["provider"] = {"options": {"heygen": {"voice_id": voice}}}
            dest = run_chain(cfg["talking"]["model"], video_openrouter, text, opts, args.out, args.wait)
        else:  # talking via HeyGen direct: your own HeyGen avatars, needs HEYGEN_API_KEY
            if not (args.avatar and args.voice):
                sys.exit("error: talking needs --photo (OpenRouter), or --avatar and --voice "
                         "(HeyGen direct; see: media.py avatars / voices)")
            dest = video_heygen(text, args.avatar, args.voice, args.out, args.wait)
    except EngineFailed as e:
        sys.exit(f"error: {e}")
    print(dest)


if __name__ == "__main__":
    main()
