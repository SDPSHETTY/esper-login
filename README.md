# 🚀 Enhanced Login CLI Tool

A beautiful, interactive terminal tool for seamless authentication to Esper cloud tenants. Transform your workflow with rich UI, session management, and intelligent tenant selection.

## ✨ Features

- 🎨 **Rich Terminal UI** - Beautiful progress indicators, formatted tables, and colorful panels
- 🔍 **Interactive Tenant Selection** - Browse and search tenants with arrow key navigation
- 📝 **Session Management** - Save, list, and switch between multiple tenant sessions
- 🤖 **Smart Matching** - Fuzzy search by tenant name or endpoint
- 🎯 **Quick Access** - Resume previous sessions instantly
- 🛡️ **Robust Error Handling** - Professional error messages with actionable guidance
- 🔄 **Backward Compatible** - All existing esper-login commands still work

---

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone <your-repo>
cd login-tool
chmod +x install.sh
./install.sh
```

### Setup

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