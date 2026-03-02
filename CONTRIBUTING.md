# Contributing to Esper Login

Thank you for your interest in contributing to the Esper Login automation tool! This project helps Esper employees and partners streamline their tenant access workflow.

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest features
- Include detailed information about your setup (macOS version, Python version, etc.)
- Provide error messages and logs when applicable
- Describe expected vs actual behavior

### Security Issues
For security-related issues involving API keys or authentication, please contact the maintainer directly rather than opening a public issue.

## 💻 Development Setup

### Prerequisites
- macOS (primary target platform)
- Python 3.9+
- Mission Control API access
- Google Chrome or Chromium

### Local Environment
```bash
# Clone your fork
git clone https://github.com/your-username/esper-login.git
cd esper-login

# Create development environment
python3 -m venv dev-env
source dev-env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy
playwright install
```

## 📝 Code Style

### Python Standards
- Follow PEP 8 style guidelines
- Use Black for code formatting: `black esper_login.py`
- Check with flake8: `flake8 esper_login.py`
- Add type hints where possible
- Include docstrings for functions

### Commit Guidelines
- Use conventional commit format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `refactor:` for code improvements
  - `test:` for adding tests

## 🔒 Security Guidelines

### API Key Handling
- **Never commit API keys** to the repository
- Use environment variables for all credentials
- Test with dummy/test keys when possible
- Document security considerations in code

### Browser Automation
- Ensure browser cleanup in all code paths
- Handle authentication errors gracefully
- Don't log sensitive authentication data

## 🧪 Testing

### Manual Testing
- Test with multiple tenant types
- Verify error handling with invalid inputs
- Test installation on fresh macOS systems
- Validate browser automation across Chrome versions

### Future Automated Testing
- Unit tests for core functions
- Integration tests for API interactions
- Security tests for credential handling

## 📋 Pull Request Process

1. **Create Feature Branch**: `git checkout -b feature/description`
2. **Make Changes**: Follow code style guidelines
3. **Test Thoroughly**: Manual testing on macOS
4. **Update Documentation**: Update README if needed
5. **Submit PR**: Clear description of changes

### PR Requirements
- Clear, descriptive title
- Detailed description of changes
- Testing notes and verification steps
- No breaking changes without discussion
- Updated documentation if applicable

## 🎯 Development Priorities

### High Priority
- **Cross-platform Support**: Linux and Windows compatibility
- **Error Handling**: Better error messages and recovery
- **Configuration**: Support for config files
- **Testing**: Automated test suite

### Medium Priority
- **Interactive Mode**: Tenant selection menu
- **Logging**: Proper logging instead of print statements
- **Performance**: Faster tenant lookup and login
- **Documentation**: More usage examples

## 🏢 Esper Context

This tool is designed for Esper employees and partners:
- Respect internal security policies
- Consider tenant-specific requirements
- Follow Esper API usage guidelines
- Maintain compatibility with Mission Control updates

## ❓ Questions

- Open GitHub issues for general questions
- Contact maintainer directly for security questions
- Review existing issues before creating new ones

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT license as the project.

---

Thank you for helping improve Esper Login automation! 🚀