import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Ganti path ini dengan nama file json Anda
SERVICE_ACCOUNT_FILE = 'emergencyalert-c61a1-firebase-adminsdk-fbsvc-d2e7ae9cdf.json'

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
credentials.refresh(Request())

access_token = credentials.token

project_id = credentials.project_id
url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; UTF-8",
}

message = {
    "message": {
        "topic": "bandara_lombok",
        "data": {
            "level": "siaga 2",
            "bandara": "Bandara Lombok"
        }
    }
}

response = requests.post(url, headers=headers, data=json.dumps(message))
print("Status:", response.status_code)
print("Response:", response.text)
