# config.py
import os

# Platforms to scan
PLATFORMS = ["github", "bitbucket", "postman"]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",                       # AWS Access Key
    r"ssh-rsa\s+[A-Za-z0-9+/=]+",              # SSH public key
    r"-----BEGIN PRIVATE KEY-----",            # Private keys
    r"[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}",  # JWT
]

# Environment tokens
GITHUB_TOKEN        = os.getenv("GITHUB_TOKEN")
BITBUCKET_USER      = os.getenv("BITBUCKET_USER")
BITBUCKET_API_TOKEN = os.getenv("BITBUCKET_API_TOKEN")
POSTMAN_API_KEY     = os.getenv("POSTMAN_API_KEY")
SLACK_WEBHOOK_URL   = os.getenv("SLACK_WEBHOOK_URL")

# Local paths
CLONE_BASE_DIR = os.path.abspath("clones")
DB_PATH         = os.path.abspath("findings.db")
