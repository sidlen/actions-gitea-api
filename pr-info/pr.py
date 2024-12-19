import requests
import json
import os

gitea_api_url = os.getenv("GITEA_API_URL")
gitea_repository = os.getenv("GITEA_REPOSITORY")
api_token = os.getenv("GITEA_API_TOKEN")
headers = {"Authorization": f"token {api_token}"}
commit_sha = os.getenv("GITEA_COMMIT_SHA")
approvers = []
approvers_emails = []

response = requests.get(f"{gitea_api_url}/repos/{gitea_repository}/pulls", headers=headers)
for pr in response.json():
    if pr["merge_commit_sha"] == commit_sha:
        pr_url = pr["html_url"]
        for approver in pr["requested_reviewers"]:
            approvers.append(approver["login"])
for approver in approvers:
    response = requests.get(f"{gitea_api_url}/users/{approver}", headers=headers)
    approvers_emails.append(response.json()["email"])
output_data = {
  "approvers_emails":approvers_emails,
  "pr_url": pr_url
}
with open('git_api.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=4, ensure_ascii=False)