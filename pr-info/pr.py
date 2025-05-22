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

def getUserEmail(user):
  response = requests.get(f"{gitea_api_url}/users/{user}", headers=headers)
  return response.json()["email"]

all_pr = requests.get(f"{gitea_api_url}/repos/{gitea_repository}/pulls", headers=headers)
for pr in all_pr.json():
    if pr["merge_commit_sha"] == commit_sha:
        target_pr = requests.get(f"{gitea_api_url}/repos/{gitea_repository}/pulls/{pr["number"]}", headers=headers)
        break
pr = target_pr.json()
pr_url = pr["html_url"]
pr_requster_email = getUserEmail(pr["user"]["login"])
pr_merge_user_email = getUserEmail(pr["merged_by"]["login"])
for approver in pr["requested_reviewers"]:
    approvers_emails.append(getUserEmail(approver["login"]))

output_data = {
  "approvers_emails":approvers_emails,
  "pr_url": pr_url,
  "pr_requster_email": pr_requster_email,
  "pr_merge_user_email": pr_merge_user_email
}
with open('gitoutput.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False)