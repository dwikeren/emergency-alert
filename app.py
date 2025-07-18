from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)
CORS(app)  # <--- PENTING agar akses dari browser diizinkan

# Load Firebase credentials
cred_path = os.path.join(os.path.dirname(__file__), 'emergencyalert-c61a1-firebase-adminsdk-fbsvc-d2e7ae9cdf.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

@app.route('/kirim-alert', methods=['POST'])
def kirim_alert():
    data = request.get_json()
    bandara = data.get('bandara')
    level = data.get('level')

    topic = f"{bandara}_{level}"
    print(f"Mengirim alert ke topik: {topic}")

    message = messaging.Message(
        notification=messaging.Notification(
            title='🚨 ALERT DARURAT',
            body=f"Level siaga: {level.upper().replace('_', ' ')}"
        ),
        topic=topic
    )

    response = messaging.send(message)
    print(f"Notifikasi berhasil dikirim: {response}")
    return jsonify({'status': 'success', 'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
