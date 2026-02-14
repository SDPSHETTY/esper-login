#!/bin/bash

# Esper Login Installation Script
# Version: 1.0.0

set -e  # Exit on any error

echo "🚀 Installing Esper Login CLI..."

# Check for Python 3.9+
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$(printf '%s\n' "3.9" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.9" ]]; then
    echo "❌ Error: Python 3.9+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check if esper_login.py exists
if [[ ! -f "esper_login.py" ]]; then
    echo "❌ Error: esper_login.py not found in current directory."
    echo "Please run this script from the esper-login repository root."
    exit 1
fi

# Check for existing installation
if command -v esper-login &> /dev/null; then
    echo "⚠️  Warning: esper-login already installed. Updating..."
fi

# Make script executable
echo "📝 Setting executable permissions..."
chmod +x esper_login.py

# Copy to system path
echo "📂 Installing to /usr/local/bin..."
if sudo cp esper_login.py /usr/local/bin/esper-login; then
    echo "✅ CLI installed successfully!"
else
    echo "❌ Error: Failed to install CLI. Check permissions."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if python3 -m pip --version &> /dev/null; then
    python3 -m pip install --user requests playwright
elif command -v pip3 &> /dev/null; then
    pip3 install --user requests playwright
elif command -v pip &> /dev/null; then
    pip install --user requests playwright
else
    echo "❌ Error: pip not found. Please install pip and try again."
    exit 1
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
if python3 -m playwright install chromium; then
    echo "✅ Playwright browsers installed successfully!"
else
    echo "⚠️  Warning: Playwright browser installation failed. Try manually:"
    echo "   python3 -m playwright install chromium"
fi

# Verify installation
echo "🔍 Verifying installation..."
if command -v esper-login &> /dev/null; then
    echo "✅ Installation complete!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Set your Mission Control API key:"
    echo "   export MISSION_CONTROL_API_KEY='your_api_key_here'"
    echo ""
    echo "2. Add to your shell profile (~/.zshrc or ~/.bash_profile):"
    echo "   echo 'export MISSION_CONTROL_API_KEY=\"your_key\"' >> ~/.zshrc"
    echo ""
    echo "3. Reload your shell:"
    echo "   source ~/.zshrc"
    echo ""
    echo "4. Test the installation:"
    echo "   esper-login --help"
    echo ""
    echo "5. Login to a tenant:"
    echo "   esper-login your-tenant-name"
    echo ""
    echo "🔒 Security Reminder:"
    echo "   Never commit your API key to version control!"
else
    echo "❌ Error: Installation verification failed. CLI not found in PATH."
    echo "Try running: sudo cp esper_login.py /usr/local/bin/esper-login"
    exit 1
fi
