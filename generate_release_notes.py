import os
import requests

GITHUB_API_BASE_URL = "https://api.github.com"
REPO_OWNER = "bluewave-labs"
REPO_NAME = "bluewave-onboarding"
GITHUB_TOKEN = os.getenv('GH_TOKEN')

def get_issues():
    url = f"{GITHUB_API_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'state': 'closed',
        'filter': 'all',
        'per_page': 100
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching issues: {response.status_code} {response.text}")

    return response.json()

def generate_release_notes():
    issues = get_issues()
    print("Fetched issues:", issues)
    release_notes = "# Release Notes\n\n"

    for issue in issues:
        if 'pull_request' in issue and issue['pull_request'] is not None and issue.get('merged_at'):
            release_notes += f"## {issue['title']}\n"
            release_notes += f"{issue['body']}\n\n"

    if release_notes == "# Release Notes\n\n":
        release_notes += "No merged pull requests found.\n"

    with open('release_notes.md', 'w') as f:
        f.write(release_notes)

if __name__ == "__main__":
    if GITHUB_TOKEN is None:
        print("Error: GH_TOKEN environment variable is not set.")
    else:
        generate_release_notes()
