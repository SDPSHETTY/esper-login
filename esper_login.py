#!/usr/bin/env python3

import os
import sys
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
    token = data.get("token") or data.get("apiKey") or data.get("key")

    if not token:
        print("ERROR: No API token returned:", data)
        sys.exit(1)

    return token


def auto_login(endpoint: str, token: str):
    login_url = f"https://{endpoint}.esper.cloud/login?siteadmin=true"

    print("\nOpening browser:", login_url)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(login_url, timeout=60000)

    # Wait for API token input
    page.wait_for_selector("input[placeholder='API Token']", timeout=60000)

    # Fill API token
    page.fill("input[placeholder='API Token']", token)

    # Click login
    page.click("button[data-testid='siteadmin-login-login-button']")

    print("\n✅ Login submitted successfully")
    print("🚀 Esper dashboard should now be open")
    print("🔒 Browser will remain open")
    print("👉 Press ENTER in terminal when you want to close it")

    # 🔒 THIS is the key line (keeps browser alive)
    input()

    print("\nClosing browser...")
    browser.close()
    playwright.stop()


def main():
    if len(sys.argv) < 2:
        print("Usage: esper-login <tenant_name>")
        sys.exit(1)

    tenant_query = sys.argv[1].lower()

    api_key = os.getenv("MC_API_KEY")
    if not api_key:
        print("ERROR: MC_API_KEY not set")
        print('Run: export MC_API_KEY="YOUR_MC_API_KEY"')
        sys.exit(1)

    print("Fetching companies...")
    companies = fetch_companies(api_key)

    items = companies.get("data")
    if not isinstance(items, list):
        print("Invalid companies response")
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

    print("\nGenerating API token...")
    token = generate_api_token(match["id"], api_key)

    auto_login(match["endpoint"], token)


if __name__ == "__main__":
    main()
