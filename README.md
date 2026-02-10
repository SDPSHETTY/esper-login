Esper Login Automation

A lightweight CLI tool to quickly log into any Esper tenant using Mission Control.

This tool:
	•	Fetches all tenants from Mission Control
	•	Generates a fresh Personal Access Token for the tenant
	•	Opens the tenant login page
	•	Automatically pastes the token and logs you in
	•	Keeps the browser open for normal dashboard usage

⸻

✨ What Problem This Solves

Normally, to log into a customer tenant you must:
	1.	Open Mission Control
	2.	Search for tenant
	3.	Click View Credentials
	4.	Generate token
	5.	Copy token
	6.	Open tenant URL
	7.	Paste token
	8.	Login

This tool reduces that to one command:
```
esper-login <tenant-name>
```


⸻

📦 Prerequisites
	•	macOS
	•	Python 3.9+
	•	Google Chrome (or Chromium)
	•	Access to Mission Control (mc.esper.io)

⸻

🔐 Mission Control API Key (REQUIRED – Per User)

⚠️ IMPORTANT
	•	Every user must use their own Mission Control API key
	•	This key is personal and machine-specific
	•	Never commit this key to GitHub
	•	This repository does NOT include any API keys

⸻

🔎 How to Get Your Mission Control API Key
	1.	Log in to https://mc.esper.io
	2.	Open Chrome DevTools → Network tab
	3.	Filter by Fetch / XHR
	4.	Click any request to:

```
mission-control-api.esper.cloud
```

	5.	In Request Headers, copy the value of:

```
authorization
```


This is your Mission Control API key.

⸻

✅ Set the API Key in Terminal

```
export MC_API_KEY="PASTE_YOUR_OWN_KEY_HERE"
```

(Optional – persist across sessions)

```
echo 'export MC_API_KEY="PASTE_YOUR_OWN_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc
```

⸻

🛠 Installation

You have two options.

⸻

OPTION 1 — Using Virtual Environment (Recommended)

1️⃣ Clone the repo

```
git clone https://github.com/SDPSHETTY/esper-login.git
cd esper-login
```

2️⃣ Create virtual environment
```
python3 -m venv .esper_venv
```
3️⃣ Activate it
```
source .esper_venv/bin/activate
```
You should see:
```
(.esper_venv)
```
4️⃣ Install dependencies
```
pip install -r requirements.txt
playwright install
```

⸻

OPTION 2 — Without Virtual Environment

⚠️ Use this only if you know what you’re doing.

```
pip3 install --user requests playwright
playwright install
```

⸻

🚀 Install CLI Command

From the project directory:

```
chmod +x esper_login.py
sudo cp esper_login.py /usr/local/bin/esper-login
```

Verify:

```
which esper-login
```

Expected:

```
/usr/local/bin/esper-login
```

⸻

▶️ Usage

```
esper-login <tenant-name>
```

What happens:
	1.	Tenant is located via Mission Control
	2.	A fresh API token is generated
	3.	Browser opens automatically
	4.	Token is pasted
	5.	Login is submitted
	6.	Browser stays open until you press ENTER

⸻

🧠 How Matching Works (Important)

Tenant lookup uses exact endpoint match first, then safe partial match.

This avoids mistakes like:
	•	dillardstest accidentally matching dillardstestdev

If multiple matches exist, the script fails safely instead of guessing.

⸻

🧪 How It Works (Internals)
	1.	Calls Mission Control:
```
GET /companies
```

	2.	Finds matching tenant by endpoint
	3.	Generates token:

```
POST /companies/{id}/personal-access-token
```

	4.	Opens:
```
https://<tenant>.esper.cloud/login?siteadmin=true
```

	5.	Uses Playwright to:
	•	Paste token
	•	Click Login

⸻

🐛 Troubleshooting

❌ MC_API_KEY missing
```
export MC_API_KEY="your-key"
```

⸻

❌ ModuleNotFoundError: requests

Make sure you installed dependencies inside the active venv:
```
pip install -r requirements.txt
```

⸻

❌ Browser opens then closes

This means:
	•	The script exited
	•	Or ENTER was pressed

The browser stays open until you press ENTER in terminal.

⸻

❌ 401 Unauthorized

Your Mission Control API key:
	•	Expired, or
	•	Belongs to a different user

Get a fresh key from DevTools.

⸻

🔐 Security Notes
	•	❌ Never commit API keys
	•	❌ Never hardcode credentials
	•	✅ Keys are read from environment only
	•	✅ Tokens are generated fresh per login

⸻

🧹 Uninstall / Reset
```
sudo rm /usr/local/bin/esper-login
rm -rf .esper_venv
```

⸻

📌 Summary

This tool allows Esper employees to:
	•	Log into any tenant in seconds
	•	Avoid manual credential handling
	•	Reduce errors and friction
	•	Stay secure
