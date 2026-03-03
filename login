#!/usr/bin/env bash
# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Activate virtual environment if it exists
if [[ -f "$SCRIPT_DIR/esper_venv/bin/activate" ]]; then
    source "$SCRIPT_DIR/esper_venv/bin/activate"
fi
exec python3 "$SCRIPT_DIR/login.py" "$@"