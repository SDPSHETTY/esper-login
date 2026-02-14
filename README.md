# Esper Login Automation

<div align="center">

**A lightweight CLI tool to quickly log into any Esper tenant using Mission Control**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Esper](https://img.shields.io/badge/Built%20for-Esper-orange.svg)](https://esper.io)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

Esper Login Automation streamlines the tenant login process for Esper employees and partners. Instead of manually navigating through Mission Control, generating tokens, and opening browsers, this tool reduces the entire workflow to a single command.

### Why This Tool?
- **⚡ Speed**: Login to any tenant in seconds
- **🔒 Security**: Generates fresh API tokens for each session
- **🎯 Accuracy**: Eliminates manual errors in tenant selection
- **🔄 Automation**: Uses Playwright for reliable browser automation

## ✨ Features

- **🚀 One-Command Login**: `esper-login tenant-name`
- **🔍 Smart Tenant Matching**: Fuzzy matching for tenant names
- **🔐 Secure Token Generation**: Fresh API tokens for each session
- **🌐 Browser Automation**: Automated login flow using Playwright
- **📊 Clear Feedback**: Informative console output and error handling
- **⚙️ Environment-Based**: Secure credential management

## 📋 Prerequisites

### System Requirements
- **macOS** (tested on Big Sur and newer)
- **Python 3.9+**
- **Google Chrome** or **Chromium**

### Required Credentials
- **Mission Control API Key** (user-specific, never commit to GitHub)
- **Esper employee access** to Mission Control

## 🛠 Installation

### Option 1: Recommended (Virtual Environment)

```bash
# Clone the repository
git clone https://github.com/SDPSHETTY/esper-login.git
cd esper-login

# Create and activate virtual environment
python3 -m venv .esper_venv
source .esper_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Make CLI available globally
chmod +x esper_login.py
sudo cp esper_login.py /usr/local/bin/esper-login
```

### Option 2: Quick Install Script

```bash
# Clone and run install script
git clone https://github.com/SDPSHETTY/esper-login.git
cd esper-login
chmod +x install.sh
./install.sh
```

### Option 3: Direct Installation (Not Recommended)

```bash
# Install dependencies globally
pip3 install --user requests playwright
playwright install chromium

# Clone and setup CLI
git clone https://github.com/SDPSHETTY/esper-login.git
cd esper-login
chmod +x esper_login.py
sudo cp esper_login.py /usr/local/bin/esper-login
```

## ⚙️ Configuration

### Set Your Mission Control API Key

**⚠️ Security Notice**: Never commit your API key to version control!

```bash
# Add to your shell profile (.zshrc, .bash_profile, etc.)
export MISSION_CONTROL_API_KEY="your_personal_api_key_here"

# Reload your shell or run:
source ~/.zshrc  # or ~/.bash_profile
```

### Verify Installation

```bash
# Check if command is available
which esper-login

# Test basic functionality (without tenant)
esper-login --help
```

## 📱 Usage

### Basic Usage

```bash
# Login to a specific tenant
esper-login my-tenant-name

# Examples with real tenant names
esper-login demo-retail
esper-login healthcare-pilot
esper-login warehouse-kiosk
```

### Advanced Usage

```bash
# Use full tenant endpoint URL
esper-login https://my-tenant.esper.cloud

# Verbose output for debugging
esper-login my-tenant --verbose

# Dry run (fetch tenant info without login)
esper-login my-tenant --dry-run
```

### Workflow Process

1. **🔍 Tenant Discovery**: Searches Mission Control for matching tenants
2. **🔐 Token Generation**: Creates fresh API token for the session
3. **🌐 Browser Launch**: Opens tenant login page automatically
4. **⚡ Auto-Login**: Completes authentication flow
5. **✅ Ready**: Tenant dashboard opens, ready for use

## 🐛 Troubleshooting

### Common Issues

**"API key not found" Error:**
```bash
# Verify environment variable
echo $MISSION_CONTROL_API_KEY

# If empty, add to shell profile
echo 'export MISSION_CONTROL_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

**"Tenant not found" Error:**
```bash
# Try partial tenant name
esper-login demo

# Use full URL if exact name fails
esper-login https://demo-tenant.esper.cloud
```

**Browser Automation Fails:**
```bash
# Reinstall Playwright browsers
playwright install chromium

# Check Chrome/Chromium installation
which google-chrome
which chromium
```

**Permission Denied:**
```bash
# Fix CLI permissions
chmod +x /usr/local/bin/esper-login

# Or reinstall with proper permissions
sudo cp esper_login.py /usr/local/bin/esper-login
sudo chmod +x /usr/local/bin/esper-login
```

### Debug Mode

```bash
# Enable verbose logging
export DEBUG_ESPER_LOGIN=1
esper-login my-tenant
```

## 👨‍💻 Development

### Local Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/SDPSHETTY/esper-login.git
cd esper-login

# Create development environment
python3 -m venv dev-env
source dev-env/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Install Playwright
playwright install
```

### Code Quality

```bash
# Format code
black esper_login.py

# Check linting
flake8 esper_login.py

# Type checking
mypy esper_login.py

# Run tests
pytest tests/
```

### Project Structure

```
esper-login/
├── 📄 README.md                # Project documentation
├── 📄 LICENSE                  # MIT license
├── 📄 requirements.txt         # Python dependencies
├── 🐍 esper_login.py          # Main CLI script
├── 📜 install.sh              # Installation script
├── 🙈 .gitignore              # Git exclusions
├── 🧪 tests/                  # Unit tests (future)
└── 📋 CHANGELOG.md            # Version history
```

## 🎯 Roadmap

### Planned Features
- **🔍 Interactive Tenant Picker**: Browse available tenants
- **📝 Configuration File**: Save preferred settings
- **🏗 Cross-Platform**: Linux and Windows support
- **📊 Usage Analytics**: Track login patterns
- **🔐 Enhanced Security**: Token rotation and expiry handling

### Version History
- **v1.0.0**: Initial release with basic login automation
- **v1.1.0**: (Planned) Interactive tenant selection
- **v1.2.0**: (Planned) Configuration file support

## 🤝 Contributing

We welcome contributions from Esper employees and partners! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors
1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and test thoroughly
4. Submit pull request with clear description

## 🔒 Security

### Security Considerations
- **API Key Protection**: Never commit API keys to version control
- **Token Management**: Fresh tokens generated for each session
- **Credential Storage**: Use environment variables only
- **Browser Security**: Automated browser runs in secure context

### Reporting Issues
For security issues, please contact the maintainer directly rather than opening public issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- **[Esper Documentation](https://docs.esper.io/)** - Complete platform documentation
- **[Mission Control](https://esper.io/mission-control/)** - Esper's management console
- **[Playwright Documentation](https://playwright.dev/python/)** - Browser automation library

---

<div align="center">
<b>Streamlining Esper Tenant Access</b><br>
<sub>Built for Esper employees and partners • Developed by Sudeep Shetty</sub>
</div>