# fetchers/clone_helper.py
import os, subprocess
from config import CLONE_BASE_DIR

def clone_repo(clone_url, name):
    dest = os.path.join(CLONE_BASE_DIR, name)
    if os.path.exists(dest):
        subprocess.run(["git", "-C", dest, "fetch"], check=True)
    else:
        os.makedirs(CLONE_BASE_DIR, exist_ok=True)
        subprocess.run(["git", "clone", clone_url, dest], check=True)
    return dest
