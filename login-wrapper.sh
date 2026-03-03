#!/bin/bash

# Enhanced Esper Login CLI Wrapper
# This script activates the virtual environment and runs the enhanced login tool

REPO_DIR="/Users/sudeepshetty/Documents/esper-login"
VENV_DIR="$REPO_DIR/.esper_venv"

# Check if we're in the repo directory, if not, change to it
if [[ "$PWD" != "$REPO_DIR" ]]; then
    cd "$REPO_DIR" || {
        echo "❌ Error: Cannot find esper-login repository at $REPO_DIR"
        exit 1
    }
fi

# Check if virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
    echo "❌ Error: Virtual environment not found at $VENV_DIR"
    echo "Please run: cd $REPO_DIR && python3 -m venv .esper_venv && source .esper_venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run the enhanced login tool
source "$VENV_DIR/bin/activate"
python3 "$REPO_DIR/login.py" "$@"