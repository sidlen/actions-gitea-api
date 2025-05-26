import requests
import json
import os
import sys

gitea_api_url = os.getenv("GITEA_API_URL")
gitea_repository = os.getenv("GITEA_REPOSITORY")
gitea_organization = os.getenv("GITEA_ORGANIZATION")
api_token = os.getenv("GITEA_API_TOKEN")
headers = {"Authorization": f"token {api_token}"}
commit_sha = os.getenv("GITEA_COMMIT_SHA")
approvers = []
approvers_emails = []

def getUserEmail_through_org(user_login):
    try:
        # Запрос списка участников организации
        response = requests.get(f"{gitea_api_url}/orgs/{gitea_organization}/members",headers=headers)
        members = response.json()
        for member in members:
            if member["username"] == user_login:
                return member["email"]
        print(f"\033[91m[ERROR]\033[0m Пользователь '{user_login}' не найден в организации '{gitea_organization}'")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\033[91m[ERROR]\033[0m Ошибка при запросе к API Gitea: {e}")
        sys.exit(1)

all_pr = requests.get(f"{gitea_api_url}/repos/{gitea_repository}/pulls", headers=headers)
for pr in all_pr.json():
    if pr["merge_commit_sha"] == commit_sha:
        target_pr = requests.get(f"{gitea_api_url}/repos/{gitea_repository}/pulls/{pr["number"]}", headers=headers)
        break
pr = target_pr.json()
pr_url = pr["html_url"]
pr_requster_email = getUserEmail_through_org(pr["user"]["login"])
pr_merge_user_email = getUserEmail_through_org(pr["merged_by"]["login"])
for approver in pr["requested_reviewers"]:
    approvers_emails.append(getUserEmail_through_org(approver["login"]))

output_data = {
  "approvers_emails":approvers_emails,
  "pr_url": pr_url,
  "pr_requster_email": pr_requster_email,
  "pr_merge_user_email": pr_merge_user_email
}
with open('gitoutput.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False)