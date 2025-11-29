Esper Auto-Login Automation — Complete Setup Guide (macOS)
Automates Esper tenant login using Mission Control API + Chromium browser.
Supports any tenant, including newly created ones.

🧩 
1. Requirements
macOS 11 or later


Python 3.10+ installed (python3 -V)


Internet connectivity


Mission Control API key



🟦 
2. INSTALLATION OPTIONS
A new user can choose:

⭐ OPTION A (Recommended): Virtual Environment
This keeps everything clean and avoids polluting system Python.

🐍 
A1. Create virtual environment
python3 -m venv ~/.esper_venv
Activate it:
source ~/.esper_venv/bin/activate
You will now see:
(.esper_venv) user@Mac %

📦 
A2. Install packages inside venv
pip install requests playwright
playwright install chromium

🟩 
A3. Continue to Step 3 (common for all)
Skip OPTION B.

⭐ OPTION B: Install WITHOUT virtual environment
Some users want global install. This is safe and fully supported.

🐍 
B1. Install Python packages globally
pip3 install --user requests playwright
Install Chromium engines:
playwright install chromium

🟩 
B2. Continue to Step 3 (common for all)

🔑 
3. Set Mission Control API Key
This key appears in your Mission Control HAR as:
authorization: <value>
Example:
export MC_API_KEY="API KEY"
Make it permanent:
echo 'export MC_API_KEY="API KEY"' >> ~/.zshrc
source ~/.zshrc

⚙️ 
4. Install the esper-login script
This script works in BOTH scenarios (venv or global).
It detects environment automatically.

📥 Install:
#!/usr/bin/env python3
import os
import sys
import json
import requests
from playwright.sync_api import sync_playwright

MC_BASE = "https://mission-control-api.esper.cloud/api/06-2020/mission-control"
COMPANIES_URL = f"{MC_BASE}/companies/?current=1&pageSize=5000"


def fetch_companies(api_key: str):
    headers = {"authorization": api_key, "accept": "*/*"}
    res = requests.get(COMPANIES_URL, headers=headers, timeout=30)
    if res.status_code != 200:
        print("ERROR fetching companies:", res.status_code, res.text)
        sys.exit(1)
    return res.json()


def generate_api_token(company_id: str, api_key: str) -> str:
    url = f"{MC_BASE}/companies/{company_id}/personal-access-token"
    headers = {"authorization": api_key, "accept": "*/*"}
    res = requests.post(url, headers=headers, timeout=30)
    if res.status_code != 200:
        print("ERROR generating token:", res.status_code, res.text)
        sys.exit(1)

    data = res.json()
    token = (
        data.get("token") or data.get("apiKey") or data.get("key")
    )

    if not token:
        print("ERROR: No token returned:", data)
        sys.exit(1)
    return token


def automated_login(endpoint: str, api_token: str):
    login_url = f"https://{endpoint}.esper.cloud/login?siteadmin=true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(login_url, wait_until="networkidle")

        selector_input = 'input[data-testid="siteadmin-login-login-input"]'
        selector_button = 'button[data-testid="siteadmin-login-login-button"]'

        page.wait_for_selector(selector_input, timeout=20000)
        page.fill(selector_input, api_token)

        page.wait_for_selector(selector_button, timeout=20000)
        page.click(selector_button)

        print("Login successful. Browser will stay open.")
        page.wait_for_timeout(5000)


def main():
    if len(sys.argv) < 2:
        print("Usage: esper-login <tenant_name>")
        sys.exit(1)

    tenant_query = sys.argv[1].lower()

    api_key = os.getenv("MC_API_KEY")
    if not api_key:
        print("ERROR: MC_API_KEY not set.")
        sys.exit(1)

    print("Fetching companies...")
    companies = fetch_companies(api_key)

    items = companies.get("data") or companies
    if not isinstance(items, list):
        print("Invalid companies response:", companies)
        sys.exit(1)

    match = None
    for c in items:
        endpoint = str(c.get("endpoint", "")).lower()
        name = str(c.get("name", "")).lower()

        if tenant_query in endpoint or tenant_query in name:
            match = c
            break

    if not match:
        print(f"Tenant '{tenant_query}' not found.")
        sys.exit(1)

    print("\n=== TENANT FOUND ===")
    print("Name:", match["name"])
    print("Endpoint:", match["endpoint"])
    print("ID:", match["id"])

    company_id = match["id"]

    print("\nGenerating API token...")
    token = generate_api_token(company_id, api_key)

    automated_login(match["endpoint"], token)


if __name__ == "__main__":
    main()

🧪 
5. Test
esper-login tenantname


🔁 
7. Updating Mission Control API Key
export MC_API_KEY="NEW_VALUE"

🧹 
8. Deactivate venv (OPTION A users)
deactivate
Reactivate later:
source ~/.esper_venv/bin/activate


