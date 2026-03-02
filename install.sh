#!/bin/bash

echo "Installing enhanced login CLI tool..."

# Make scripts executable
chmod +x login.py
chmod +x login

# Install the Python script and wrapper
sudo cp login.py /usr/local/bin/login.py
sudo cp login /usr/local/bin/login
sudo chmod +x /usr/local/bin/login.py
sudo chmod +x /usr/local/bin/login

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Running first-time browser install..."
playwright install chromium

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  login                    # Interactive tenant selection"
echo "  login <tenant_name>      # Login to specific tenant"
echo "  login --list             # Show active sessions"
echo "  login --switch <tenant>  # Switch to existing session"
echo "  login --help             # Show detailed help"
echo ""
echo "💡 Don't forget to set your MC_API_KEY:"
echo "    export MC_API_KEY=\"your-api-key-here\""
echo ""