#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
    printf 'No se encontró el intérprete: %s\n' "$PYTHON" >&2
    exit 1
fi

if [[ ! -x ".venv/bin/python" ]]; then
    "$PYTHON" -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r requirements.txt
exec python main.py
