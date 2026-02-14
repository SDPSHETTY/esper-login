# Changelog

All notable changes to the Esper Login project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-02-13

### Added
- 🚀 **Initial Release**: CLI tool for automated Esper tenant login
- 🔍 **Tenant Discovery**: Automatic tenant search via Mission Control API
- 🔐 **Token Generation**: Fresh API token creation for each session
- 🌐 **Browser Automation**: Playwright-powered login automation
- ⚙️ **Environment Integration**: Secure API key management via environment variables
- 📋 **Error Handling**: Comprehensive error checking and user feedback

### Technical Implementation
- **Python 3.9+ Support**: Modern Python with type hints and async support
- **Cross-Browser Support**: Chromium-based browser automation
- **Mission Control Integration**: API-driven tenant and token management
- **Security Focus**: Environment-based credential storage

### Installation
- **Virtual Environment Support**: Recommended isolated installation
- **Global CLI Installation**: System-wide `esper-login` command
- **Automated Setup**: `install.sh` script for quick deployment
- **Prerequisites Check**: Clear documentation of system requirements

### Usage
- **Simple Command**: `esper-login tenant-name` workflow
- **Flexible Matching**: Supports partial tenant names and full URLs
- **Clear Feedback**: Informative console output and progress indication
- **Error Recovery**: Helpful error messages and troubleshooting guidance

---

## Planned Features

### [1.1.0] - Future Release
- **Interactive Tenant Picker**: Browse and select from available tenants
- **Configuration File**: Save user preferences and default settings
- **Enhanced Error Messages**: More specific guidance for common issues
- **Verbose Mode**: Detailed logging for debugging and troubleshooting

### [1.2.0] - Future Release
- **Cross-Platform Support**: Linux and Windows compatibility
- **Tenant Favorites**: Quick access to frequently used tenants
- **Session Management**: Handle multiple concurrent tenant sessions
- **API Key Rotation**: Automated key refresh and management

### [2.0.0] - Major Release
- **GUI Interface**: Optional graphical interface for non-CLI users
- **Multi-User Support**: Shared installation with user-specific configs
- **Advanced Automation**: Custom workflow scripts and integrations
- **Audit Logging**: Track usage and access patterns for compliance

---

## Development History

### Key Milestones
- **Project Inception**: Internal tool to streamline Esper employee workflows
- **Playwright Integration**: Replaced manual browser steps with automation
- **Mission Control API**: Direct integration for tenant discovery and token management
- **Open Source Release**: Made available for broader Esper community

### Technical Decisions
- **Python Choice**: Rapid development with excellent library ecosystem
- **Playwright over Selenium**: Better reliability and performance for automation
- **Environment Variables**: Secure credential storage without config files
- **CLI-First Design**: Optimized for developer workflow integration

---

**Legend:**
- 🚀 Major features and releases
- 🔍 Discovery and search functionality
- 🔐 Security and authentication
- 🌐 Browser and web automation
- ⚙️ Configuration and setup
- 📋 Error handling and user experience
- 💻 Development and technical improvements
- 🎯 Performance and optimization