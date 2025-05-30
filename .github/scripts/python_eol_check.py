#!/usr/bin/env python3
"""
Python EOL Check Script

This script checks if the Python version used in the project is approaching its End of Life (EOL) date.
If the EOL date is within 30 days, it creates a GitHub issue to notify the maintainers.
"""

import argparse
import sys
from datetime import datetime

import httpx
from github import Github


def get_python_version():
    """
    Read the Python version from the .python-version file.

    Returns:
        str: The Python version.
    """
    try:
        with open(".python-version") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: .python-version file not found.")
        sys.exit(1)


def get_eol_info(python_version: str):
    """
    Get the EOL information for the specified Python version.

    Args:
        python_version (str): The Python version to check.

    Returns:
        dict: The EOL information.
    """
    url = f"https://endoflife.date/api/python/{python_version}.json"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching EOL information: {e}")
        sys.exit(1)


def calculate_days_until_eol(eol_date: str) -> int:
    """
    Calculate the number of days until the EOL date.

    Args:
        eol_date (str): The EOL date in YYYY-MM-DD format.

    Returns:
        int: The number of days until the EOL date.
    """
    current_date = datetime.now().date()
    eol_date_obj = datetime.strptime(eol_date, "%Y-%m-%d").date()
    return (eol_date_obj - current_date).days


def check_existing_issue(github_client: Github, repo_owner: str, repo_name: str, python_version: str) -> bool:
    """
    Check if an issue about the Python EOL already exists.

    Args:
        github_client (Github): The GitHub client.
        repo_owner (str): The repository owner.
        repo_name (str): The repository name.
        python_version (str): The Python version.

    Returns:
        bool: True if an issue already exists, False otherwise.
    """
    repo = github_client.get_repo(f"{repo_owner}/{repo_name}")
    issues = repo.get_issues(state="open", creator="github-actions[bot]")

    for issue in issues:
        if f"Python {python_version}" in issue.title and "End of Life date" in issue.title:
            print(f"Issue already exists: #{issue.number}")
            return True

    return False


def create_issue(
    github_client: Github, repo_owner: str, repo_name: str, python_version: str, eol_date: str, days_until_eol: int
) -> int:
    """
    Create a GitHub issue about the Python EOL.

    Args:
        github_client (Github): The GitHub client.
        repo_owner (str): The repository owner.
        repo_name (str): The repository name.
        python_version (str): The Python version.
        eol_date (str): The EOL date.
        days_until_eol (int): The number of days until the EOL date.

    Returns:
        int: The issue number.
    """
    repo = github_client.get_repo(f"{repo_owner}/{repo_name}")

    issue_title = f"Python {python_version} will reach End of Life date on {eol_date}"
    issue_body = f"""
# Python Version End of Life Reminder

The current Python version {python_version} used in this project will reach its **End of Life date** on **{eol_date}**,
which is **{days_until_eol}** days from now.

Please consider upgrading to a newer Python version to ensure the security and stability of the project.

## Related Information

- [Python Version End of Life Information](https://endoflife.date/python)
- [Python Official Download Page](https://www.python.org/downloads/)

*This issue was created by an automated workflow*
"""

    issue = repo.create_issue(title=issue_title, body=issue_body, labels=["python", "maintenance"])

    print(f"Issue created: #{issue.number}")
    return issue.number


def main():
    """
    Main function to check Python EOL and create an issue if needed.
    """
    parser = argparse.ArgumentParser(description="Check Python EOL and create GitHub issue if needed.")
    parser.add_argument("--repo-owner", required=True, help="Repository owner")
    parser.add_argument("--repo-name", required=True, help="Repository name")
    parser.add_argument("--github-token", required=True, help="GitHub token")
    args = parser.parse_args()

    # Get Python version
    python_version = get_python_version()
    print(f"Python version: {python_version}")

    # Get EOL information
    eol_info = get_eol_info(python_version)
    eol_date = eol_info["eol"]
    print(f"EOL date: {eol_date}")

    # Calculate days until EOL
    days_until_eol = calculate_days_until_eol(eol_date)
    print(f"Days until EOL: {days_until_eol}")

    # Check if we need to create an issue
    if days_until_eol <= 30:
        print("Python version is approaching EOL, checking if issue already exists...")

        # Initialize GitHub client
        github_client = Github(args.github_token)

        # Check if issue already exists
        if _issue_exists := check_existing_issue(github_client, args.repo_owner, args.repo_name, python_version):
            print("Issue already exists, skipping creation.")
        else:
            # Create issue if it doesn't exist
            print("Creating issue...")
            create_issue(github_client, args.repo_owner, args.repo_name, python_version, eol_date, days_until_eol)
    else:
        print(f"Python version is not approaching EOL (more than 30 days left: {days_until_eol} days).")


if __name__ == "__main__":
    main()
