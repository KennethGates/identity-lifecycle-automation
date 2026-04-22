import requests
import os
from dotenv import load_dotenv

load_dotenv()

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
domain = os.getenv("DOMAIN")

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}

token_response = requests.post(token_url, data=token_data)
token_json = token_response.json()
access_token = token_json.get("access_token")

if not access_token:
    print("Failed to get access token")
    print(token_json)
    exit()

print("Access token acquired")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

new_user = {
    "accountEnabled": True,
    "displayName": "Brenda HR 2",
    "mailNickname": "brendahr2",
    "userPrincipalName": f"brendahr2@{domain}",
    "passwordProfile": {
        "forceChangePasswordNextSignIn": True,
        "password": "TempPass123!"
    },
    "department": "HR",
    "jobTitle": "HR Analyst"
}

response = requests.post(
    "https://graph.microsoft.com/v1.0/users",
    headers=headers,
    json=new_user
)

print("Create User Status Code:", response.status_code)
print(response.json())

if response.status_code != 201:
    print("User creation failed. Stopping.")
    exit()

user_id = response.json().get("id")
group_name = "HR-Group"

group_response = requests.get(
    f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{group_name}'",
    headers=headers
)

group_data = group_response.json()

if "value" not in group_data or len(group_data["value"]) == 0:
    print("Group not found")
    exit()

group_id = group_data["value"][0]["id"]
print(f"Found group: {group_name}")

add_member_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
member_data = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"}

add_response = requests.post(add_member_url, headers=headers, json=member_data)
print("Add to Group Status Code:", add_response.status_code)

if add_response.status_code == 204:
    print(f"User added to {group_name}")
else:
    print("Failed to add user to group")
    print(add_response.text)
