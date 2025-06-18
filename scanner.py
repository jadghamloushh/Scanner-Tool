import os
import sqlite3
import logging
import requests
import subprocess
import json
from github import GithubException
from clients.github_client import gh, list_user_repos as gh_repos
from clients.bitbucket_client import bb, list_user_repos as bb_repos
from clients.postman_client import list_collections as pm_colls
from fetchers.clone_helper import clone_repo
from fetchers.postman_fetcher import download_collection
from detection.regex_detector import find_with_regex
from detection.external_tools import run_detect_secrets, run_gitleaks
from config import DB_PATH, SLACK_WEBHOOK_URL

# 1. Setup logging
logging.basicConfig(level=logging.INFO)

# 2. Initialize DB connection
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY,
        platform TEXT,
        target TEXT,
        file_path TEXT,
        detector TEXT,
        secret TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()

# 3. Record a finding
def record(platform, target, file_path, detector, secret):
    c.execute(
        "INSERT INTO findings(platform,target,file_path,detector,secret) VALUES (?,?,?,?,?)",
        (platform, target, file_path, detector, secret)
    )
    conn.commit()

# 4. Mitigation / notification
def create_github_issue(repo_full, file_path, secret):
    repo = gh.get_repo(repo_full)

    title = "🚨 Secret Detected: Action Required"
    body = f"""
I detected a potential secret in `{file_path}`:

```
{secret[:80]}...
```

Please rotate the credential and remove it from the repository.
"""
    try:
        issue = repo.create_issue(title=title, body=body)
        logging.info("Created GitHub issue #%s in %s", issue.number, repo_full)
    except GithubException as e:
        msg = e.data.get("message", str(e))
        logging.error("Failed to create issue on %s: %s", repo_full, msg)


def create_bitbucket_issue(full_name, file_path, secret):
    payload = {
        "title": "🚨 Secret Detected: Action Required",
        "content": {
            "raw": f"""
Potential secret in `{file_path}`:

```
{secret[:80]}...
```
"""
        }
    }
    try:
        bb.create_issue(full_name, data=payload)
        logging.info("Created Bitbucket issue in %s", full_name)
    except Exception as e:
        logging.error("Failed to create Bitbucket issue on %s: %s", full_name, e)


def notify_postman_leak(coll_name, file_path, secret):
    text = f""":warning: Secret detected in Postman collection `{coll_name}` (file: {file_path})

```
{secret[:80]}...
```"""
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": text})
        logging.info("Sent Slack alert for Postman collection %s", coll_name)
    except Exception as e:
        logging.error("Failed to send Slack alert for %s: %s", coll_name, e)

# 5. Scan functions
def scan_github():
    for repo in gh_repos():
        path = clone_repo(repo.clone_url, repo.full_name.replace("/", "_"))
        # Regex-based detection
        for root, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    txt = open(fp, errors="ignore").read()
                except Exception:
                    continue
                for patt, secret in find_with_regex(txt):
                    record("github", repo.full_name, fp, "regex", secret)
                    create_github_issue(repo.full_name, fp, secret)
        # detect-secrets
        ds = run_detect_secrets(path)
        for fn, secrets_list in ds.items():
            for secret in secrets_list:
                record("github", repo.full_name, fn, "detect-secrets", secret)
                create_github_issue(repo.full_name, fn, secret)
        # gitleaks
        leaks = run_gitleaks(path)
        for leak in leaks:
            record("github", repo.full_name, leak.get("File"), "gitleaks", leak.get("Secret"))
            create_github_issue(repo.full_name, leak.get("File"), leak.get("Secret"))


def scan_bitbucket():
    for r in bb_repos():
        full = r.get("full_name")
        clone_entry = next((c for c in r.get("links", {}).get("clone", []) if c.get("name") == "https"), None)
        if not clone_entry:
            continue
        clone_url = clone_entry.get("href")
        logging.info("Scanning Bitbucket repo %s", full)
        path = clone_repo(clone_url, full.replace("/", "_"))
        # Regex-based detection
        for root, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    txt = open(fp, errors="ignore").read()
                except Exception:
                    continue
                for patt, secret in find_with_regex(txt):
                    record("bitbucket", full, fp, "regex", secret)
                    create_bitbucket_issue(full, fp, secret)
        # detect-secrets
        ds = run_detect_secrets(path)
        for fn, secrets_list in ds.items():
            for secret in secrets_list:
                record("bitbucket", full, fn, "detect-secrets", secret)
                create_bitbucket_issue(full, fn, secret)
        # gitleaks
        leaks = run_gitleaks(path)
        for leak in leaks:
            record("bitbucket", full, leak.get("File"), "gitleaks", leak.get("Secret"))
            create_bitbucket_issue(full, leak.get("File"), leak.get("Secret"))


def scan_postman():
    for coll in pm_colls():
        uid, name = coll.get("uid"), coll.get("name")
        logging.info("Downloading Postman collection %s", name)
        path = download_collection(uid, name)
        try:
            txt = open(path).read()
        except Exception:
            continue
        for patt, secret in find_with_regex(txt):
            record("postman", name, path, "regex", secret)
            notify_postman_leak(name, path, secret)


# def send_summary_to_slack():
#     count = c.execute("SELECT COUNT(*) FROM findings WHERE DATE(timestamp)=DATE('now')").fetchone()[0]
#     msg = f":warning: *{count}* new secret findings today."
#     try:
#         requests.post(SLACK_WEBHOOK_URL, json={"text": msg})
#         logging.info("Sent daily summary to Slack")
#     except Exception as e:
#         logging.error("Failed to send summary to Slack: %s", e)


if __name__ == "__main__":
    scan_github()
    # scan_bitbucket()
    #scan_postman()
    #send_summary_to_slack()
    conn.close()
