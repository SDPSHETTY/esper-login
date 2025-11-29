# Esper Login Automation

A simple automation tool to:
- Fetch tenants from Mission Control  
- Generate Personal Access Tokens  
- Auto-launch browser & log in using Playwright  
- Quickly switch between any customer tenant  

---

## Installation (Two Options)

---

# OPTION 1 — **Using Virtual Environment (Recommended)**

### 1. Create project folder
```bash
mkdir esper-login
cd esper-login

2. Create virtual environment

python3 -m venv .esper_venv

3. Activate it

source .esper_venv/bin/activate

4. Install dependencies

pip install requests playwright
playwright install


⸻

OPTION 2 — WITHOUT Virtual Environment

If you don’t want venv:

pip3 install --user requests playwright
playwright install

⚠️ Must use python3 and pip3.
⚠️ Avoid sudo pip (breaks macOS).

⸻

⚙️ Setup

1. Export your Mission Control API key

export MC_API_KEY="YOUR_MC_KEY_HERE"

Example:

export MC_API_KEY="4ad91703-6dd3-4d52-9377-c2d6a31ee723"

You can add it permanently:

echo 'export MC_API_KEY="4ad91703-6dd3-4d52-9377-c2d6a31ee723"' >> ~/.zshrc


⸻

📌 Install CLI wrapper

Create:

/usr/local/bin/esper-login

Paste:

#!/bin/bash
python3 /usr/local/bin/esper_login.py "$@"

Make executable:

sudo chmod +x /usr/local/bin/esper-login


⸻

📜 Python Script

Save the script below as:

/usr/local/bin/esper_login.py

#!/usr/bin/env python3
import os
import sys
import requests
from playwright.sync_api import sync_playwright

MC_COMPANY_API = "https://mission-control-api.esper.cloud/api/06-2020/mission-control/companies"
TOKEN_API_TEMPLATE = "https://mission-control-api.esper.cloud/api/06-2020/mission-control/companies/{}/personal-access-token"

def fetch_companies(api_key):
    headers = {"authorization": api_key, "accept": "*/*"}
    res = requests.get(MC_COMPANY_API, headers=headers)

    if res.status_code != 200:
        print(f"ERROR fetching companies: {res.status_code}")
        print(res.text)
        sys.exit(1)

    return res.json()

def generate_api_token(company_id, api_key):
    token_url = TOKEN_API_TEMPLATE.format(company_id)
    headers = {"authorization": api_key, "accept": "*/*"}
    
    res = requests.post(token_url, headers=headers)

    if res.status_code != 200:
        print("\nERROR generating API token")
        print(res.status_code, res.text)
        sys.exit(1)

    data = res.json()
    return data.get("apiKey")

def auto_login(endpoint, token):
    login_url = f"https://{endpoint}.esper.cloud/login?siteadmin=true"

    print("\nOpening browser:", login_url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(login_url)

        # Wait for API Token field
        page.wait_for_selector("input[placeholder='API Token']")
        page.fill("input[placeholder='API Token']", token)

        # Click Login button
        page.click("button[data-testid='siteadmin-login-login-button']")

        print("Login submitted!")
        page.wait_for_timeout(5000)

def main():
    if len(sys.argv) < 2:
        print("Usage: esper-login <tenant-name>")
        sys.exit(1)

    tenant_name = sys.argv[1].lower()
    api_key = os.getenv("MC_API_KEY")

    if not api_key:
        print("ERROR: MC_API_KEY missing")
        sys.exit(1)

    print("Fetching companies...")
    companies = fetch_companies(api_key)
    items = companies.get("data", [])

    tenant = None
    for c in items:
        if c.get("endpoint", "").lower() == tenant_name:
            tenant = c
            break

    if not tenant:
        print(f"Tenant '{tenant_name}' not found")
        sys.exit(1)

    print("\n=== TENANT FOUND ===")
    print("Name:", tenant.get("name"))
    print("Endpoint:", tenant.get("endpoint"))
    print("ID:", tenant.get("id"))

    print("\nGenerating API token...")
    token = generate_api_token(tenant["id"], api_key)

    print("API Key:", token)

    auto_login(tenant["endpoint"], token)

if __name__ == "__main__":
    main()


⸻

🧪 Example Usage

esper-login guvrqy

esper-login dinedev

esper-login tkdwq


⸻

🔥 How It Works
	1.	Reads tenant list from Mission Control
	2.	Finds correct tenant by endpoint
	3.	Generates fresh token using personal-access-token API
	4.	Launches login page
	5.	Pastes token
	6.	Auto-clicks Login

⸻

🐛 Troubleshooting

If you get MC_API_KEY missing:

export MC_API_KEY="your-key"

If Playwright fails:

playwright install

If script permission denied:

sudo chmod +x /usr/local/bin/esper-login
