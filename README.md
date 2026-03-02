# 🚀 Enhanced Login CLI Tool

<div align="center">

**A beautiful, interactive terminal tool for seamless authentication to Esper cloud tenants**

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
- [Examples](#examples)
- [Session Management](#session-management)
- [Rich Terminal Features](#rich-terminal-features)
- [Migration from esper-login](#migration-from-esper-login)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

Transform your Esper tenant login workflow with rich UI, session management, and intelligent tenant selection. This enhanced version preserves the excellent 3-function architecture while adding professional terminal experience and advanced features.

## ✨ Features

- 🎨 **Rich Terminal UI** - Beautiful progress indicators, formatted tables, and colorful panels
- 🔍 **Interactive Tenant Selection** - Browse and search tenants with arrow key navigation
- 📝 **Session Management** - Save, list, and switch between multiple tenant sessions
- 🤖 **Smart Matching** - Fuzzy search by tenant name or endpoint
- 🎯 **Quick Access** - Resume previous sessions instantly
- 🛡️ **Robust Error Handling** - Professional error messages with actionable guidance
- 🔄 **Backward Compatible** - All existing esper-login commands still work

## Prerequisites

- Python 3.9+
- Mission Control API Key
- macOS (primary support)

## 🚀 Installation

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

## Configuration

Export your Mission Control API key:
```bash
export MC_API_KEY="your-api-key-here"

# Add to your shell profile for persistence
echo 'export MC_API_KEY="your-api-key-here"' >> ~/.zshrc
```

---

## 💡 Usage

### Interactive Mode (Recommended)
```bash
login
```
Choose from a beautiful tenant list with search and navigation.

### Direct Login
```bash
login <tenant_name>        # Login to specific tenant
login dinedev             # Partial name matching
login mycompany-prod      # Endpoint matching
```

### Session Management
```bash
login --list              # Show active sessions
login --switch <endpoint> # Switch to existing session
login --help              # Show detailed help
```

---

## 🎯 Examples

### First-time Interactive Login
```bash
$ login
┌── 🔍 Interactive Tenant Selection ────────────────────┐
│ No tenant specified or multiple matches found.       │
│ Select a tenant from the interactive list:           │
└───────────────────────────────────────────────────────┘

┏━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ # ┃ Name          ┃ Endpoint      ┃
┡━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 1 │ Acme Corp     │ acme-prod     │
│ 2 │ Dev Testing   │ dinedev       │
│ 3 │ Staging Env   │ staging-test  │
└───┴───────────────┴───────────────┘

Enter tenant number (1-3) or 'q' to quit: 2
```

### Quick Access to Known Tenant
```bash
$ login dinedev
┌── 🏢 Tenant Found ─────────────────────────────────────┐
│ ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Field    ┃ Value                                 ┃ │
│ ┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ Name     │ Dev Testing                           │ │
│ │ Endpoint │ dinedev                               │ │
│ │ ID       │ abc123-def456                         │ │
│ └──────────┴───────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘

┌── 🎉 Login Success ────────────────────────────────────────┐
│ ✅ Login submitted successfully                           │
│ 🚀 Esper dashboard should now be open                    │
│ 🔒 Browser will remain open                              │
└───────────────────────────────────────────────────────────────┘
```

### Session Management
```bash
$ login --list
┌── 📝 Active Sessions ──────────────────────────────────────┐
│ ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓         │
│ ┃ Endpoint   ┃ Name          ┃ Last Used      ┃         │
│ ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩         │
│ │ dinedev    │ Dev Testing   │ 2024-01-15 14:30 │       │
│ │ acme-prod  │ Acme Corp     │ 2024-01-15 09:15 │       │
│ └────────────┴───────────────┴─────────────────────┘      │
└────────────────────────────────────────────────────────────┘

$ login --switch dinedev
Switching to session: Dev Testing (dinedev)
```

---

## 🎨 Rich Terminal Features

### Beautiful Progress Indicators
- Animated spinners during API calls
- Real-time status updates
- Smooth transitions and feedback

### Professional Error Handling
```
┌── 🚨 API Error ─────────────────────────────────────┐
│ ERROR fetching companies:                          │
│ Status Code: 401                                   │
│ Response: Invalid API key                          │
└────────────────────────────────────────────────────────┘
```

### Success Celebrations
```
┌── 🎉 Login Success ────────────────────────────────┐
│ ✅ Login submitted successfully                   │
│ 🚀 Esper dashboard should now be open            │
│ 🔒 Browser will remain open                      │
└───────────────────────────────────────────────────────┘
```

---

## 📁 Configuration

### Automatic Configuration
The tool automatically creates and manages configuration at:
```
~/.login/config.json
```

### Configuration Structure
```json
{
  "active_sessions": {
    "dinedev": {
      "tenant": {...},
      "token": "...",
      "login_time": "2024-01-15T14:30:00",
      "last_used": "2024-01-15T14:30:00"
    }
  },
  "favorites": [],
  "recent_tenants": ["dinedev", "acme-prod"],
  "preferences": {
    "theme": "default",
    "auto_close_browser": false
  }
}
```

---

## 🔧 Advanced Features

### Environment Variables
- `MC_API_KEY` - Mission Control API Key (required)
- `LOGIN_CLASSIC_MODE=1` - Use original esper-login behavior

### Backward Compatibility
All existing esper-login commands work unchanged:
```bash
# These still work exactly as before
login dinedev
login mycompany
```

### Session Persistence
- Sessions automatically saved after successful login
- Quick switching between recent tenants
- Automatic token refresh handling

---

## 🚨 Troubleshooting

### Common Issues

**API Key Missing**
```bash
export MC_API_KEY="your-api-key-here"
```

**Playwright Browser Issues**
```bash
playwright install chromium
```

**Permission Denied**
```bash
chmod +x login
sudo chmod +x /usr/local/bin/login
```

**Dependencies Missing**
```bash
pip3 install -r requirements.txt
```

---

## 🏗️ Architecture

### Core Functions (Preserved from Original)
- `fetch_companies()` - API client with enhanced UI feedback
- `generate_api_token()` - Token generation with progress indicators
- `auto_login()` - Browser automation with rich status updates

### Enhanced Features
- `interactive_tenant_selector()` - Rich TUI for tenant selection
- `load_config()` / `save_config()` - Configuration management
- `save_session()` - Session persistence
- `show_active_sessions()` - Session listing with formatting

---

## 📊 Comparison: Before vs After

| Feature | Original esper-login | Enhanced login |
|---------|---------------------|----------------|
| UI | Plain text | Rich terminal UI with colors, tables, panels |
| Tenant Selection | Command line argument only | Interactive picker + CLI args |
| Error Messages | Basic print statements | Professional error panels with guidance |
| Session Management | None | Full session persistence and switching |
| Help System | Basic usage line | Comprehensive help with examples |
| Progress Feedback | Minimal | Animated spinners and status updates |
| Multiple Matches | Error and exit | Interactive selection |
| Configuration | Environment variables only | JSON config with preferences |

---

## 🤝 Migration from esper-login

### Automatic Migration
The enhanced tool is fully backward compatible:

1. **Existing Commands Work**: All `esper-login` commands work with `login`
2. **No Config Changes**: Uses same `MC_API_KEY` environment variable
3. **Same Core Logic**: Preserved the excellent 3-function architecture
4. **Enhanced Experience**: Adds features without breaking existing workflows

### Side-by-Side Installation
You can run both tools during transition:
- Keep existing `esper-login` installation
- Install new `login` tool in parallel
- Gradually switch workflows
- Remove old tool when comfortable

---

## 🚀 What's New

### Version 2.0 Features
- 🎨 Beautiful rich terminal UI
- 🔍 Interactive tenant browser
- 📝 Session management system
- 🤖 Smart fuzzy search
- 🎯 Quick session switching
- 🛡️ Enhanced error handling
- 📚 Comprehensive help system
- 🔄 Full backward compatibility

### Performance Improvements
- Cached session data for faster switching
- Optimized API calls
- Reduced browser startup time
- Efficient tenant filtering

---

## 📈 Development

### Project Structure
```
login-tool/
├── login.py              # Enhanced main script
├── login                 # CLI wrapper
├── requirements.txt      # Dependencies
├── install.sh           # Installation script
└── README.md            # This file
```

### Dependencies
- `requests` - HTTP client
- `playwright` - Browser automation
- `rich` - Terminal UI
- `click` - CLI framework
- `keyring` - Secure storage

---

## 💫 Why Choose Enhanced Login?

### For Individual Developers
- **Faster Workflow**: Quick tenant switching saves minutes per day
- **Better UX**: Beautiful interface makes repetitive tasks enjoyable
- **Error Recovery**: Clear error messages with actionable solutions

### For Teams
- **Consistency**: Standardized login process across team members
- **Discoverability**: Interactive mode helps find available tenants
- **Session Sharing**: Easy to communicate tenant endpoints

### For Organizations
- **Professional**: Rich UI reflects attention to quality and detail
- **Maintainable**: Clean architecture built on solid foundation
- **Extensible**: Easy to add custom features and integrations

---

**🎉 Ready to transform your Esper login experience? Install the enhanced login tool today!**

### Alternative Installation Methods
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
