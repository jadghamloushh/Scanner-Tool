## ✨ Features

- **Multi-engine detection** – Detect-Secrets, TruffleHog, GitLeaks, custom regexes
- **Cross-platform** – Works on Windows, macOS, Linux (Python 3.8+)
- **One-click notifications** – Slack webhooks + auto-GitHub-issue template
- **Pluggable response hooks** – stubs for AWS key de-activation, GitHub PAT rotation
- **SQLite findings DB** – easy to query or feed into BI tools
- **Flask dashboard** – live feed of the last 50 leaks
- **Responsible-disclosure defaults** – redacts secrets, obeys rate limits, no public shaming

---

## ⚙️ Requirements

| Component        | How to install                                                                               | Needed for                |
| ---------------- | -------------------------------------------------------------------------------------------- | ------------------------- |
| **Python 3.8 +** | Pre-installed on macOS/Linux, [`python.org`](https://www.python.org/) for Windows            | Everything                |
| **Git**          | `brew install git`, `sudo apt install git`, or [Git for Windows](https://gitforwindows.org/) | Cloning targets           |
| **GitLeaks**     | Only external binary—see **Step 4** below                                                    | One of the three scanners |

Everything else is pulled from **PyPI**.

---

## 🚀 Quick-start (all OSes)

````bash
# 1. Clone Token-Guardian
git clone https://github.com/jadghamloushh/Scanner-Tool.git
cd Scanner-Tool

# 2. Make a virtual environment
# Linux/macOS  ➜
python3 -m venv .venv && source .venv/bin/activate
# Windows (PowerShell) ➜
python -m venv .venv; .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip wheel setuptools

# 3. Install Python deps
pip install -r requirements.txt

# 4. Install GitLeaks
# macOS  ➜  brew install gitleaks
# Linux  ➜  sudo apt install gitleaks
# Windows ➜ download ZIP from Releases, put gitleaks.exe on PATH

---

## 📝 Make a `.env` and put your keys

```dotenv
GITHUB_TOKEN=yourtoken
BITBUCKET_USER=yourtoken
BITBUCKET_API_TOKEN=yourtoken
POSTMAN_API_KEY=yourtoken
````

`````

````

---

## 🏃‍♂️ Usage

### Launch the Flask dashboard

```bash
python dashboard.py
# then open http://localhost:5000
```

### Launch the Flask dashboard

```bash
export GITHUB_TOKEN="you token"
python scanner.py
```

---

### 🔧 Choosing which GitHub repositories to scan

`clients/github_client.py` controls the _input list_ for the scanner.
By default it returns a **single hard-coded repo**:

```python
from github import Github
from config import GITHUB_TOKEN

gh = Github(GITHUB_TOKEN)

def list_user_repos():
    # current demo target
    return [gh.get_repo("jadghamloushh/scanner-test")]
    #to scan all repos do this:
    return [gh.get_user().get_repos()]

---

````
`````
