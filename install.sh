#!/bin/bash

# Enhanced Esper Login Installation Script
# Version: 2.0.0

set -e  # Exit on any error

echo "🚀 Installing Enhanced Login CLI..."

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

# Check if enhanced login files exist
if [[ ! -f "login.py" ]]; then
    echo "❌ Error: login.py not found in current directory."
    echo "Please run this script from the esper-login repository root."
    exit 1
fi

# Check for existing installation
if command -v login &> /dev/null; then
    echo "⚠️  Warning: login already installed. Updating..."
fi

if command -v esper-login &> /dev/null; then
    echo "⚠️  Warning: esper-login already installed. Updating..."
fi

# Make scripts executable
echo "📝 Setting executable permissions..."
chmod +x login.py
chmod +x login

# Install the Python script and wrapper
echo "📂 Installing enhanced CLI to /usr/local/bin..."
if sudo cp login.py /usr/local/bin/login.py && sudo cp login /usr/local/bin/login; then
    sudo chmod +x /usr/local/bin/login.py
    sudo chmod +x /usr/local/bin/login
    echo "✅ Enhanced CLI installed successfully!"
else
    echo "❌ Error: Failed to install CLI. Check permissions."
    echo "Alternative: Install without sudo by updating PATH to include current directory"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if python3 -m pip --version &> /dev/null; then
    python3 -m pip install --user requests playwright rich click keyring
elif command -v pip3 &> /dev/null; then
    pip3 install --user requests playwright rich click keyring
elif command -v pip &> /dev/null; then
    pip install --user requests playwright rich click keyring
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
if command -v login &> /dev/null; then
    echo ""
    echo "🎉 Enhanced Login CLI Installation Complete!"
    echo ""
    echo "📋 Next Steps:"
    echo ""
    echo "1. Set your Mission Control API key:"
    echo "   export MC_API_KEY='your_api_key_here'"
    echo ""
    echo "2. Add to your shell profile (~/.zshrc or ~/.bash_profile):"
    echo "   echo 'export MC_API_KEY=\"your_key\"' >> ~/.zshrc"
    echo ""
    echo "3. Reload your shell:"
    echo "   source ~/.zshrc"
    echo ""
    echo "4. Try the enhanced features:"
    echo "   login --help         # Show comprehensive help"
    echo "   login               # Interactive tenant selection"
    echo "   login <tenant>      # Login to specific tenant"
    echo "   login --list        # Show active sessions"
    echo ""
    echo "🎨 New Features:"
    echo "   • Rich terminal UI with colors and progress indicators"
    echo "   • Interactive tenant selection with search"
    echo "   • Session management and switching"
    echo "   • Professional error handling"
    echo "   • Full backward compatibility"
    echo ""
    echo "🔒 Security Reminder:"
    echo "   Never commit your API key to version control!"
    echo ""
    echo "📚 Documentation: Check README.md for comprehensive usage guide"
else
    echo "❌ Error: Installation verification failed. CLI not found in PATH."
    echo "Try running: sudo cp login.py /usr/local/bin/login && sudo chmod +x /usr/local/bin/login"
    exit 1
fi