import argparse
import os
import sys

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-title", required=True)
    args = parser.parse_args()
    pr_title = args.pr_title

    words = pr_title.split(":", 1)
    issue_key = words[0]

    jira_url = os.getenv("JIRA_URL")
    if not jira_url:
        raise Exception("Missing JIRA URL")
    jira_email = os.getenv("JIRA_EMAIL")
    if not jira_email:
        raise Exception("Missing JIRA account's email address")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_api_token:
        raise Exception("Missing JIRA TOKEN key")

    response = requests.get(
        f"{jira_url}/rest/api/latest/issue/{issue_key}",
        auth=(jira_email, jira_api_token))

    if response.status_code == 404:
        raise Exception(f"No JIRA issue found: {issue_key}")

    if response.status_code != 200:
        raise Exception(f"Unexpected response code: {response.status_code} (text: {response.text})")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"Operation failed: {str(ex)}", file=sys.stderr)
        sys.exit(1)
