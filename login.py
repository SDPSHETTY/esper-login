#!/usr/bin/env python3

import os
import sys
import json
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

# Rich UI imports for enhanced terminal experience
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import keyring
from datetime import datetime


class EsperLoginError(Exception):
    """Custom exception for Esper Login application errors"""
    pass

MC_BASE = "https://mission-control-api.esper.cloud/api/06-2020/mission-control"
COMPANIES_URL = f"{MC_BASE}/companies/?current=1&pageSize=5000"

# Initialize rich console
console = Console()

# Configuration paths
CONFIG_DIR = Path.home() / ".login"
CONFIG_FILE = CONFIG_DIR / "config.json"


def fetch_companies(api_key: str):
    """Fetch companies from Mission Control API with rich UI feedback"""
    with console.status("[bold green]Fetching companies...") as status:
        headers = {"authorization": api_key, "accept": "*/*"}
        try:
            res = requests.get(COMPANIES_URL, headers=headers, timeout=30)
            if res.status_code != 200:
                sanitized_response = sanitize_error_message(res.text)
                console.print(Panel(
                    f"[bold red]ERROR fetching companies:[/bold red]\n"
                    f"Status Code: {res.status_code}\n"
                    f"Response: {sanitized_response}",
                    title="🚨 API Error",
                    border_style="red"
                ))
                raise EsperLoginError(f"Failed to fetch companies: HTTP {res.status_code}")
            return res.json()
        except requests.RequestException as e:
            console.print(Panel(
                f"[bold red]Network error:[/bold red] {str(e)}",
                title="🌐 Connection Error",
                border_style="red"
            ))
            raise EsperLoginError(f"Network error fetching companies: {str(e)}")


def generate_api_token(company_id: str, api_key: str) -> str:
    """Generate API token with enhanced progress feedback"""
    with console.status("[bold blue]Generating API token...") as status:
        url = f"{MC_BASE}/companies/{company_id}/personal-access-token"
        headers = {"authorization": api_key, "accept": "*/*"}

        try:
            res = requests.post(url, headers=headers, timeout=30)
            if res.status_code != 200:
                sanitized_response = sanitize_error_message(res.text)
                console.print(Panel(
                    f"[bold red]ERROR generating token:[/bold red]\n"
                    f"Status Code: {res.status_code}\n"
                    f"Response: {sanitized_response}",
                    title="🔑 Token Generation Error",
                    border_style="red"
                ))
                raise EsperLoginError(f"Failed to generate token: HTTP {res.status_code}")

            data = res.json()
            token = data.get("token") or data.get("apiKey") or data.get("key")

            if not token:
                sanitized_data = sanitize_error_message(str(data))
                console.print(Panel(
                    f"[bold red]ERROR: No API token returned:[/bold red]\n{sanitized_data}",
                    title="🔑 Token Missing",
                    border_style="red"
                ))
                raise EsperLoginError("No API token found in response")

            return token
        except requests.RequestException as e:
            console.print(Panel(
                f"[bold red]Network error:[/bold red] {str(e)}",
                title="🌐 Connection Error",
                border_style="red"
            ))
            raise EsperLoginError(f"Network error generating token: {str(e)}")


def auto_login(endpoint: str, token: str):
    """Enhanced browser login with rich UI feedback"""
    login_url = f"https://{endpoint}.esper.cloud/login?siteadmin=true"

    console.print(Panel(
        f"[bold cyan]Opening browser:[/bold cyan]\n{login_url}",
        title="🌐 Browser Launch",
        border_style="cyan"
    ))

    playwright = sync_playwright().start()
    browser = None

    try:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        with console.status("[bold yellow]Loading login page..."):
            page.goto(login_url, timeout=60000)

        with console.status("[bold yellow]Waiting for login form..."):
            # Wait for API token input
            page.wait_for_selector("input[placeholder='API Token']", timeout=60000)

        with console.status("[bold yellow]Filling credentials..."):
            # Fill API token
            page.fill("input[placeholder='API Token']", token)

        with console.status("[bold yellow]Submitting login..."):
            # Click login
            page.click("button[data-testid='siteadmin-login-login-button']")

        # Success celebration
        console.print()
        console.print(Panel(
            "[bold green]✅ Login submitted successfully[/bold green]\n"
            "[bold blue]🚀 Esper dashboard should now be open[/bold blue]\n"
            "[bold yellow]🔒 Browser will remain open[/bold yellow]",
            title="🎉 Login Success",
            border_style="green"
        ))

        console.print("\n[bold cyan]👉 Press ENTER in terminal when you want to close the browser[/bold cyan]")

        # Keep browser alive
        input()

        console.print("[bold yellow]Closing browser...[/bold yellow]")

    except Exception as e:
        console.print(Panel(
            f"[bold red]Browser automation error:[/bold red] {str(e)}",
            title="🎭 Playwright Error",
            border_style="red"
        ))
        raise EsperLoginError(f"Browser automation failed: {str(e)}")

    finally:
        # Ensure cleanup always happens
        if browser:
            try:
                browser.close()
            except Exception:
                pass  # Ignore cleanup errors
        try:
            playwright.stop()
        except Exception:
            pass  # Ignore cleanup errors


def display_tenant_info(tenant_data):
    """Display tenant information in a beautiful table"""
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Field", style="cyan", width=12)
    table.add_column("Value", style="green")

    table.add_row("Name", tenant_data["name"])
    table.add_row("Endpoint", tenant_data["endpoint"])
    table.add_row("ID", tenant_data["id"])

    console.print()
    console.print(Panel(
        table,
        title="🏢 Tenant Found",
        border_style="green"
    ))


def interactive_tenant_selector(companies_list):
    """Interactive tenant selection with rich TUI"""
    console.print(Panel(
        "[bold cyan]No tenant specified or multiple matches found.[/bold cyan]\n"
        "[yellow]Select a tenant from the interactive list:[/yellow]",
        title="🔍 Interactive Tenant Selection",
        border_style="cyan"
    ))

    # Create a table of available tenants
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="cyan")
    table.add_column("Endpoint", style="green")

    items = companies_list.get("data", [])
    for i, company in enumerate(items[:20]):  # Limit to first 20 for readability
        table.add_row(
            str(i + 1),
            company.get("name", "N/A"),
            company.get("endpoint", "N/A")
        )

    console.print(table)

    # Get user selection
    while True:
        try:
            choice = Prompt.ask(
                "\n[bold cyan]Enter tenant number (1-{}) or 'q' to quit[/bold cyan]".format(
                    min(len(items), 20)
                )
            )

            if choice.lower() == 'q':
                console.print("[yellow]Goodbye! 👋[/yellow]")
                raise KeyboardInterrupt("User requested exit")

            choice_num = int(choice)
            if 1 <= choice_num <= min(len(items), 20):
                selected_tenant = items[choice_num - 1]
                return selected_tenant
            else:
                console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number or 'q' to quit.[/red]")


def load_config():
    """Load configuration from ~/.login/config.json"""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(exist_ok=True)
        default_config = {
            "active_sessions": {},
            "favorites": [],
            "recent_tenants": [],
            "preferences": {
                "theme": "default",
                "auto_close_browser": False
            }
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        console.print("[yellow]Warning: Invalid config file. Using defaults.[/yellow]")
        return {"active_sessions": {}, "favorites": [], "recent_tenants": [], "preferences": {}}


def save_config(config_data):
    """Save configuration to ~/.login/config.json"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)


def migrate_tokens_to_keyring():
    """Migrate any existing plaintext tokens to keyring storage"""
    config = load_config()
    sessions = config.get("active_sessions", {})
    migrated_count = 0

    for endpoint, session_data in sessions.items():
        # Check if token exists in plaintext
        if "token" in session_data:
            token = session_data["token"]
            service_name = get_keyring_service_name(endpoint)

            try:
                # Store token in keyring
                keyring.set_password(service_name, "api_token", token)
                # Remove token from config
                del session_data["token"]
                migrated_count += 1
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to migrate token for {endpoint}: {str(e)}[/yellow]")

    if migrated_count > 0:
        save_config(config)
        console.print(f"[green]Migrated {migrated_count} tokens to secure storage.[/green]")

    return migrated_count


def get_keyring_service_name(endpoint):
    """Generate a consistent keyring service name for an endpoint"""
    return f"esper-login.{endpoint}"


def sanitize_error_message(text):
    """Sanitize error messages to prevent API key or token leakage"""
    if not text:
        return text

    # Common patterns that might contain sensitive data
    sensitive_patterns = [
        # API keys (various formats)
        (r'["\']?api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_.-]{20,}["\']?', 'API_KEY_REDACTED'),
        (r'["\']?token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_.-]{20,}["\']?', 'TOKEN_REDACTED'),
        (r'["\']?authorization["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_.-]{20,}["\']?', 'AUTH_REDACTED'),
        # Long alphanumeric strings that might be tokens/keys (20+ chars)
        (r'\b[a-zA-Z0-9_.-]{32,}\b', 'SENSITIVE_DATA_REDACTED'),
        # JWT patterns
        (r'eyJ[a-zA-Z0-9_.-]+', 'JWT_REDACTED'),
    ]

    import re
    sanitized = str(text)

    for pattern, replacement in sensitive_patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    # Limit length to prevent extremely long error dumps
    if len(sanitized) > 500:
        sanitized = sanitized[:500] + "...[truncated]"

    return sanitized


def save_session(tenant_info, token):
    """Save session information with secure token storage"""
    config = load_config()

    # Store token securely in keyring
    service_name = get_keyring_service_name(tenant_info["endpoint"])
    try:
        keyring.set_password(service_name, "api_token", token)
    except Exception as e:
        console.print(Panel(
            f"[bold red]Failed to store token securely:[/bold red] {str(e)}\n"
            f"[yellow]Token will not be saved for future use.[/yellow]",
            title="🔐 Keyring Error",
            border_style="red"
        ))

    # Store session metadata (without token)
    session_data = {
        "tenant": tenant_info,
        "login_time": datetime.now().isoformat(),
        "last_used": datetime.now().isoformat()
    }

    config["active_sessions"][tenant_info["endpoint"]] = session_data

    # Add to recent tenants (keep last 10)
    endpoint = tenant_info["endpoint"]
    if endpoint in config["recent_tenants"]:
        config["recent_tenants"].remove(endpoint)
    config["recent_tenants"].insert(0, endpoint)
    config["recent_tenants"] = config["recent_tenants"][:10]

    save_config(config)


def main():
    """Enhanced main function with interactive features"""
    try:
        # Migrate any existing plaintext tokens to secure storage
        migrate_tokens_to_keyring()

        # Handle different CLI modes
        if len(sys.argv) >= 2:
            if sys.argv[1] in ['--list', '-l']:
                show_active_sessions()
                return
            elif sys.argv[1] in ['--switch', '-s'] and len(sys.argv) >= 3:
                switch_to_session(sys.argv[2])
                return
            elif sys.argv[1] in ['--help', '-h']:
                show_enhanced_help()
                return

        # Check for API key
        api_key = os.getenv("MC_API_KEY")
        if not api_key:
            console.print(Panel(
                "[bold red]ERROR: MC_API_KEY not set[/bold red]\n\n"
                "[yellow]Please set your Mission Control API key:[/yellow]\n"
                "[cyan]export MC_API_KEY=\"YOUR_MC_API_KEY\"[/cyan]",
                title="🔑 API Key Missing",
                border_style="red"
            ))
            return

        # Fetch companies
        companies = fetch_companies(api_key)

        items = companies.get("data")
        if not isinstance(items, list):
            console.print(Panel(
                "[bold red]Invalid companies response[/bold red]",
                title="🚨 API Response Error",
                border_style="red"
            ))
            raise EsperLoginError("Invalid companies response format")

        # Handle tenant selection
        if len(sys.argv) < 2:
            # No argument provided - show interactive selector
            selected_tenant = interactive_tenant_selector(companies)
        else:
            # Search for tenant by query
            tenant_query = sys.argv[1].lower()
            matches = []

            for c in items:
                endpoint = str(c.get("endpoint", "")).lower()
                name = str(c.get("name", "")).lower()

                if tenant_query in endpoint or tenant_query in name:
                    matches.append(c)

            if not matches:
                console.print(Panel(
                    f"[bold red]Tenant '{tenant_query}' not found.[/bold red]\n\n"
                    f"[yellow]Try running '[cyan]login[/cyan]' without arguments for interactive selection.[/yellow]",
                    title="🔍 Tenant Not Found",
                    border_style="red"
                ))
                return
            elif len(matches) == 1:
                selected_tenant = matches[0]
            else:
                # Multiple matches - show interactive selector with filtered results
                console.print(f"[yellow]Multiple tenants match '{tenant_query}':[/yellow]")
                filtered_companies = {"data": matches}
                selected_tenant = interactive_tenant_selector(filtered_companies)

        # Display selected tenant info
        display_tenant_info(selected_tenant)

        # Generate token and login
        console.print()
        token = generate_api_token(selected_tenant["id"], api_key)

        # Save session info
        save_session(selected_tenant, token)

        auto_login(selected_tenant["endpoint"], token)

    except EsperLoginError as e:
        console.print(Panel(
            f"[bold red]Login failed:[/bold red] {str(e)}",
            title="❌ Error",
            border_style="red"
        ))
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"[bold red]Unexpected error:[/bold red] {str(e)}",
            title="💥 Unexpected Error",
            border_style="red"
        ))
        sys.exit(1)


def show_active_sessions():
    """Display active sessions in a formatted table"""
    config = load_config()
    sessions = config.get("active_sessions", {})

    if not sessions:
        console.print(Panel(
            "[yellow]No active sessions found.[/yellow]\n\n"
            "[cyan]Run 'login <tenant>' to create your first session.[/cyan]",
            title="📝 Active Sessions",
            border_style="yellow"
        ))
        return

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Endpoint", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Last Used", style="yellow")

    for endpoint, session_data in sessions.items():
        tenant = session_data["tenant"]
        last_used = datetime.fromisoformat(session_data["last_used"])
        table.add_row(
            endpoint,
            tenant["name"],
            last_used.strftime("%Y-%m-%d %H:%M")
        )

    console.print(Panel(
        table,
        title="📝 Active Sessions",
        border_style="blue"
    ))


def switch_to_session(endpoint):
    """Switch to an existing session"""
    config = load_config()
    sessions = config.get("active_sessions", {})

    if endpoint not in sessions:
        console.print(Panel(
            f"[bold red]Session for '{endpoint}' not found.[/bold red]\n\n"
            "[yellow]Available sessions:[/yellow]",
            title="❌ Session Not Found",
            border_style="red"
        ))
        show_active_sessions()
        return

    session_data = sessions[endpoint]
    tenant = session_data["tenant"]

    # Retrieve token securely from keyring
    service_name = get_keyring_service_name(endpoint)
    try:
        token = keyring.get_password(service_name, "api_token")
        if not token:
            console.print(Panel(
                f"[bold red]Token not found in secure storage for '{endpoint}'.[/bold red]\n"
                f"[yellow]Please run 'login {endpoint}' to authenticate again.[/yellow]",
                title="🔐 Token Missing",
                border_style="red"
            ))
            return
    except Exception as e:
        console.print(Panel(
            f"[bold red]Failed to retrieve token from secure storage:[/bold red] {str(e)}\n"
            f"[yellow]Please run 'login {endpoint}' to authenticate again.[/yellow]",
            title="🔐 Keyring Error",
            border_style="red"
        ))
        return

    console.print(f"[green]Switching to session: {tenant['name']} ({endpoint})[/green]")
    display_tenant_info(tenant)

    # Update last used time
    session_data["last_used"] = datetime.now().isoformat()
    save_config(config)

    auto_login(endpoint, token)


def show_enhanced_help():
    """Display enhanced help with rich formatting"""
    help_text = """
[bold blue]Enhanced Login CLI Tool[/bold blue]

[bold green]Basic Usage:[/bold green]
  [cyan]login[/cyan]                    Interactive tenant selection
  [cyan]login <tenant>[/cyan]         Login to specific tenant
  [cyan]login <partial_name>[/cyan]   Search and login to tenant

[bold green]Session Management:[/bold green]
  [cyan]login --list[/cyan]           Show active sessions
  [cyan]login --switch <endpoint>[/cyan]  Switch to existing session

[bold green]Examples:[/bold green]
  [dim]login[/dim]                    # Interactive mode
  [dim]login dinedev[/dim]            # Login to tenant with 'dinedev' in name/endpoint
  [dim]login --list[/dim]             # Show all active sessions
  [dim]login --switch mycompany[/dim] # Switch to existing 'mycompany' session

[bold green]Configuration:[/bold green]
  Config file: [cyan]~/.login/config.json[/cyan]
  Sessions, favorites, and preferences are automatically saved.

[bold yellow]Environment Variables:[/bold yellow]
  [cyan]MC_API_KEY[/cyan]             Mission Control API Key (required)
  [cyan]LOGIN_CLASSIC_MODE[/cyan]     Set to 1 for original behavior
    """

    console.print(Panel(
        help_text,
        title="🚀 Login CLI Help",
        border_style="blue"
    ))


if __name__ == "__main__":
    main()