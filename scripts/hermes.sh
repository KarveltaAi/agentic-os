#!/usr/bin/env bash
# Thin wrapper: talk to the LOCAL Hermes 3 model via Ollama (tier "local").
# Equivalent to: python scripts/llm.py --tier local "<prompt>"
# Usage:
#   scripts/hermes.sh "Say ready if you can hear me"
#   cat notes.txt | scripts/hermes.sh --stdin
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [ -z "$PYTHON_BIN" ]; then
    echo "No python3/python found on PATH. Install Python 3 to use the Hermes sidecar." >&2
    exit 1
fi

if [ "${1:-}" = "--stdin" ]; then
    exec "$PYTHON_BIN" "$SCRIPT_DIR/llm.py" --tier local --stdin
elif [ $# -gt 0 ]; then
    exec "$PYTHON_BIN" "$SCRIPT_DIR/llm.py" --tier local "$*"
else
    echo 'Usage: scripts/hermes.sh "<prompt>"   (or: cat file | scripts/hermes.sh --stdin)' >&2
    exit 1
fi
