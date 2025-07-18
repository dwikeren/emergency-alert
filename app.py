from flask import Flask, request, jsonify
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = Flask(__name__)

@app.route("/kirim-alert", methods=["POST"])
def kirim_alert():
    try:
        SERVICE_ACCOUNT_FILE = 'emergencyalert-c61a1-firebase-adminsdk-fbsvc-d2e7ae9cdf.json'
        SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        credentials.refresh(Request())

        access_token = credentials.token
        project_id = credentials.project_id
        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        data = request.json
        level = data.get("level")
        bandara_input = data.get("bandara")

        if not level or not bandara_input:
            return jsonify({"error": "Level dan Bandara harus disertakan."}), 400

        # Bersihkan nama bandara → jadi lowercase + underscore
        bandara_clean = bandara_input.lower().replace(" ", "_")
        topic = f"bandara_{bandara_clean}"

        message = {
            "message": {
                "topic": topic,
                "data": {
                    "level": level,
                    "bandara": bandara_input
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; UTF-8",
        }

        response = requests.post(url, headers=headers, data=json.dumps(message))

        return jsonify({
            "status_code": response.status_code,
            "response": response.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
