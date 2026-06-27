import os
import requests
from datetime import datetime, timedelta, timezone
import sys

def get_recent_github_repos():
    """
    Fetches recent GitHub repositories related to AI and Open Source.
    """
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=30)
    time_str = time_threshold.strftime('%Y-%m-%dT%H:%M:%SZ')

    query = f"ai open-source created:>{time_str}"
    url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"Fetching data from GitHub: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    else:
        print(f"Error fetching from GitHub: {response.status_code} - {response.text}")
        return []

def create_github_issue(repos):
    """
    Creates a GitHub issue with the list of repositories. 
    GitHub will automatically send an email notification for this new issue.
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    github_repository = os.environ.get("GITHUB_REPOSITORY") # Format: owner/repo

    if not github_token or not github_repository:
        print("GITHUB_TOKEN or GITHUB_REPOSITORY environment variables are missing.")
        sys.exit(1)

    if not repos:
        print("No new repositories found in the last 30 minutes. No issue created.")
        return

    # Prepare Issue Content
    title = f"GitHub Update: New AI & Open Source Repositories ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    body = f"Found {len(repos)} new/updated repositories in the last 30 minutes:\n\n"
    for repo in repos:
        body += f"### [{repo.get('full_name')}]({repo.get('html_url')})\n"
        body += f"- **Description**: {repo.get('description') or 'No description provided.'}\n"
        body += f"- **Stars**: {repo.get('stargazers_count')} | **Language**: {repo.get('language') or 'N/A'}\n\n"

    url = f"https://api.github.com/repos/{github_repository}/issues"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body
    }

    try:
        print(f"Creating issue in {github_repository}...")
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Issue created successfully: {response.json().get('html_url')}")
        else:
            print(f"Failed to create issue: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to make request: {e}")

if __name__ == "__main__":
    recent_repos = get_recent_github_repos()
    create_github_issue(recent_repos)
