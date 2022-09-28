import argparse
import os
import sys
import json
import logging

import requests

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[%(levelname)-8s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-title", required=True)
    args = parser.parse_args()
    pr_title = args.pr_title

    words = pr_title.split(":", 1)
    issue_key = words[0].strip()

    jira_url = os.getenv("JIRA_URL")
    if not jira_url:
        raise Exception("Missing JIRA URL")
    jira_email = os.getenv("JIRA_EMAIL")
    if not jira_email:
        raise Exception("Missing JIRA account's email address")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if not jira_api_token:
        raise Exception("Missing JIRA TOKEN key")

    logger.info(f"Searching for issue '{issue_key}' in JIRA server located at {jira_url}")

    response = requests.get(
        f"{jira_url}/rest/api/latest/issue/{issue_key}",
        auth=(jira_email, jira_api_token))

    if response.status_code == 404:
        raise Exception(f"No JIRA issue found: {issue_key}")

    if response.status_code != 200:
        raise Exception(f"Unexpected response code: {response.status_code} (text: {response.text})")

    try:
        issue_title = response.json()["fields"]["summary"]
    except Exception:
        logger.warning(f"Failed retrieving summary of issue {issue_key}", exc_info=True)
        issue_title = "N/A"

    logger.info(f"Found issue {issue_key}: {issue_title}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"Operation failed: {str(ex)}", file=sys.stderr)
        sys.exit(1)
