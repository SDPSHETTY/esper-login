#!/bin/bash

echo "Installing esper-login..."

chmod +x esper_login.py
sudo cp esper_login.py /usr/local/bin/esper-login
sudo chmod +x /usr/local/bin/esper-login

echo "Running first-time browser install..."
playwright install chromium

echo "Done! Run: esper-login <tenant>"
