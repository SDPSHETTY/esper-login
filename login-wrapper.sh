#!/bin/bash

# Enhanced Esper Login CLI Wrapper
# This script activates the virtual environment and runs the enhanced login tool

# Get the directory where this script is located (works regardless of where it's called from)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR"
VENV_DIR="$REPO_DIR/esper_venv"

# Change to the repository directory
cd "$REPO_DIR" || {
    echo "❌ Error: Cannot access esper-login repository at $REPO_DIR"
    exit 1
}

# Check if virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
    echo "❌ Error: Virtual environment not found at $VENV_DIR"
    echo "Please run: cd $REPO_DIR && python3 -m venv esper_venv && source esper_venv/bin/activate && pip install -r requirements.txt && playwright install chromium"
    exit 1
fi

# Activate virtual environment and run the enhanced login tool
source "$VENV_DIR/bin/activate"
python3 "$REPO_DIR/login.py" "$@"