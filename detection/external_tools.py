# detection/external_tools.py
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List

# ───────────────────────── Detect-Secrets ──────────────────────────
from detect_secrets.core.scan import scan_file
from detect_secrets.settings import Settings


def run_detect_secrets(repo_path: str) -> Dict[str, List[str]]:

    settings = Settings() 
    findings: Dict[str, List[str]] = {}

    for root, _, files in os.walk(repo_path):
        for fname in files:
            fp = os.path.join(root, fname)
            try:
                secrets = scan_file(fp, settings=settings)
            except Exception:
                continue
            if secrets:
                findings[fp] = [s.secret_value for s in secrets]

    return findings


# ─────────────────────────── Gitleaks ──────────────────────────────
def run_gitleaks(repo_path: str) -> List[dict]:
    """
    Run the Gitleaks CLI and return the list of leak objects (even if leaks were found).
    """
    cmd = [
        "gitleaks",
        "detect",
        "--source",
        str(Path(repo_path).resolve()),
        "--report-format",
        "json",
        "--exit-code",
        "0",
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True)
    if not completed.stdout.strip():
        return []  # no leaks or JSON output

    return json.loads(completed.stdout)

def run_trufflehog(repo_path: str):

    cmd = [
        "trufflehog",
        "filesystem",               # local scan
        repo_path,
        "--json",                   # JSON output
        "--no-update",              # skip self-update prompt
    ]
    # TruffleHog always prints each finding as one JSON line
    output = subprocess.check_output(cmd, text=True)
    findings = [json.loads(line) for line in output.splitlines() if line.strip()]
    return findings