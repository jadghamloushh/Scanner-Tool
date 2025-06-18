````markdown
# 🛡️ Token-Guardian

**Token-Guardian** is a cross-platform, all-Python toolkit that scans public (or local) code repositories and log streams for leaked secrets—API keys, OAuth tokens, database URIs, SSH keys—and raises an immediate alert.  
It wraps three battle-tested scanners (Detect-Secrets, TruffleHog v3, GitLeaks) plus your own regex/ML rules, then records every finding in SQLite and (optionally) files a GitHub issue or Slack notification.  
A tiny Flask dashboard (`dashboard.py`) visualises everything in real time.

---

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

```bash
# 1. Clone Token-Guardian
git clone https://github.com/<your-user>/token-guardian.git
cd token-guardian

# 2. Make a virtual environment
# Linux/macOS  ➜
python3 -m venv .venv && source .venv/bin/activate
# Windows (PowerShell) ➜
# python -m venv .venv; .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip wheel setuptools

# 3. Install Python deps
pip install -r requirements.txt        # or:  pip install -e .

# 4. Install GitLeaks (only non-Python part)
# macOS  ➜  brew install gitleaks
# Linux  ➜  sudo apt install gitleaks
# Windows ➜ download ZIP from Releases, put gitleaks.exe on PATH

# 5. Create a .env file with your tokens
cp .env.example .env    # then open .env and fill in values

# 6. Scan something!
python scanner.py --repo https://github.com/torvalds/linux -o report.json
# or, if installed with `pip install -e .`:
# secretscan --repo https://github.com/torvalds/linux -o report.json

# 7. View the dashboard (optional)
python dashboard.py     # opens http://localhost:5000
```
````

---

## 📝 `.env` file (minimal)

```dotenv
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxx
SLACK_WEBHOOK=https://hooks.slack.com/services/XXX/YYY/ZZZ
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

_No secrets are committed to Git; `python-dotenv` loads them at runtime._

---

## 🏃‍♂️ Usage

### Scan a public repo and write JSON

```bash
secretscan --repo https://github.com/alice/project -o findings.json
```

### Watch a local log folder for real-time leaks

```bash
python -m monitor.file_watch /var/log/myapp
```

### Poll Elasticsearch (ELK) for leaks every 15 s

```bash
python -m monitor.elk_watch --index app-logs --interval 15
```

### Launch the Flask dashboard

```bash
python dashboard.py
# then open http://localhost:5000
```

---

## 🔄 Updating Token-Guardian

```bash
git pull
pip install -e . --upgrade
```

---

## ❌ Uninstall

```bash
deactivate            # leave the venv
rm -rf .venv          # delete virtual env
rm -rf token-guardian # remove source clone
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-rule`)
3. Add tests in `tests/` (pytest)
4. Run `pre-commit run --all-files`
5. Submit a PR 🎉

---

## 🔒 Responsible disclosure / Ethics

- The scanner stores **only redacted fingerprints** of tokens by default (first 4 / last 4).
- GitHub issues are created as private security advisories when the calling PAT has permission.
- No attempt is made to exploit or validate secrets against live services unless you **explicitly** enable validator plugins.

---

## 📄 License

MIT – see [`LICENSE`](LICENSE).

Happy scanning! ☕

```

```
