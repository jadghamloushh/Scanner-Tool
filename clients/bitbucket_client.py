# clients/bitbucket_client.py
from atlassian.bitbucket.cloud import Cloud
from config import BITBUCKET_USER, BITBUCKET_API_TOKEN

bb = Cloud(
    url="https://api.bitbucket.org/",     # this is optional; Cloud defaults to api.bitbucket.org
    username=BITBUCKET_USER,
    password=BITBUCKET_API_TOKEN,
    cloud=True                            # make sure you’re using the Cloud endpoints
)

def list_user_repos():
    """
    Returns a list of dicts with "full_name" & "links"
    for every repo in your personal workspace.
    """
    workspace = bb.workspaces.get(BITBUCKET_USER)
    return [
        {"full_name": repo["full_name"], "links": repo["links"]}
        for repo in workspace.repositories.each()
    ]
