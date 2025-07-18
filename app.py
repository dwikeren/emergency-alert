from flask import Flask, request, jsonify
from flask_cors import CORS
import json, requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
        bandara = data.get("bandara")

        if not level or not bandara:
            return jsonify({"error": "Level dan Bandara harus disertakan."}), 400

        message = {
            "message": {
                "topic": "bandara_lombok",
                "data": {
                    "level": level,
                    "bandara": bandara
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
