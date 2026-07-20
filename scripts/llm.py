#!/usr/bin/env python3
"""Tiered model router for offloaded (non-Claude) work. Reads tier config from
ops/model-routing.json: local (Ollama, free), budget/frontier (OpenRouter).
Called by the Hermes crew and Otto (model-router agent), and by
scripts/hermes.ps1 / scripts/hermes.sh as a thin `--tier local` wrapper.
Stdlib only - no pip dependencies, so the free "local" tier always works
out of the box. Prints the model's raw response to stdout; everything else
(errors, status) goes to stderr, so stdout stays clean for programmatic use."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROUTING_PATH = REPO_ROOT / "ops" / "model-routing.json"
ENV_PATH = REPO_ROOT / ".env"
PLACEHOLDER_MARKERS = ("VERIFY_ID", "PLACEHOLDER", "CHEAP_MODEL_ID_HERE", "SET_AFTER_VERIFYING_IDS")


def load_dotenv(path: Path) -> None:
    """Populate os.environ from a .env file, without overwriting vars already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_routing() -> dict:
    if not ROUTING_PATH.exists():
        sys.exit(f"error: routing config not found at {ROUTING_PATH}")
    return json.loads(ROUTING_PATH.read_text(encoding="utf-8"))


def is_placeholder(model_id) -> bool:
    return not isinstance(model_id, str) or any(marker in model_id for marker in PLACEHOLDER_MARKERS)


def call_ollama(model: str, prompt: str, timeout: int) -> str:
    body = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        sys.exit(
            f"error: could not reach Ollama at localhost:11434 ({e}). "
            f"Is the Ollama app/service running, and has `ollama pull {model}` completed?"
        )
    return data.get("response", "").strip()


def call_openrouter(model: str, prompt: str, timeout: int) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        sys.exit(
            "error: OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key "
            "(RUNBOOK Phase 4B), or use --tier local."
        )
    body = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": prompt}]}
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"error: OpenRouter request failed ({e.code}): {e.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach OpenRouter ({e}).")
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        sys.exit(f"error: unexpected OpenRouter response shape: {data}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a prompt to a local or OpenRouter model tier.")
    parser.add_argument("--tier", required=True, choices=["local", "budget", "frontier"])
    parser.add_argument("--stdin", action="store_true", help="read the prompt from stdin instead of argv")
    parser.add_argument("--timeout", type=int, default=300, help="request timeout in seconds (default 300)")
    parser.add_argument("prompt", nargs="*", help="the prompt text (quote it, or use --stdin for long input)")
    args = parser.parse_args()

    if args.stdin:
        prompt = sys.stdin.read().strip()
    else:
        prompt = " ".join(args.prompt).strip()
    if not prompt:
        sys.exit("error: no prompt given (pass it as an argument or use --stdin)")

    load_dotenv(ENV_PATH)
    routing = load_routing()
    tier_cfg = routing.get("tiers", {}).get(args.tier)
    if not tier_cfg:
        sys.exit(f"error: tier '{args.tier}' not found in {ROUTING_PATH}")

    model = tier_cfg.get("model")
    if is_placeholder(model):
        sys.exit(
            f"tier '{args.tier}' is not configured yet - {ROUTING_PATH} still has a placeholder "
            f"model ID. See RUNBOOK Phase 4B. Falling back: use --tier local."
        )

    if tier_cfg.get("provider") == "ollama":
        result = call_ollama(model, prompt, args.timeout)
    elif tier_cfg.get("provider") == "openrouter":
        result = call_openrouter(model, prompt, args.timeout)
    else:
        sys.exit(f"error: unknown provider '{tier_cfg.get('provider')}' for tier '{args.tier}'")

    print(result)


if __name__ == "__main__":
    main()
