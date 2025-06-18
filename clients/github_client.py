from github import Github
from config import GITHUB_TOKEN

gh = Github(GITHUB_TOKEN)

def list_user_repos():
    return [ gh.get_repo("jadghamloushh/scanner-test") ]
