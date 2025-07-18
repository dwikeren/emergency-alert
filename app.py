from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'API aktif'

@app.route('/kirim-alert', methods=['POST'])
def kirim_alert():
    data = request.get_json()
    bandara = data.get('bandara')
    level = data.get('level')

    # Lakukan proses kirim alert ke Firebase atau logika lainnya
    print(f"[ALERT] Bandara: {bandara} | Level: {level}")

    return jsonify({'status': 'success', 'message': 'Alert dikirim'}), 200

if __name__ == '__main__':
    app.run()
