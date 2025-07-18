from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Inilah kunci agar bisa diakses dari Netlify

FCM_API_KEY = "ISI_DENGAN_SERVER_KEY_FIREBASE_MU"

@app.route("/")
def home():
    return "API Siap!"

@app.route("/kirim-alert", methods=["POST"])
def kirim_alert():
    try:
        data = request.get_json()
        bandara = data.get("bandara", "")
        level = data.get("level", "")

        headers = {
            "Authorization": "key=" + FCM_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "to": "/topics/" + bandara,
            "priority": "high",
            "data": {
                "level": level
            }
        }

        res = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)
        return jsonify({"success": True, "status_code": res.status_code, "response": res.json()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
