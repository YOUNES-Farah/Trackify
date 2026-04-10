from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

# Fichier pour enregistrer les logs
LOG_FILE = "logs.json"

# Liste des utilisateurs autorisés
authorized_users = [
    {"name": "John Doe", "uid": "123456789"},
    {"name": "Jane Smith", "uid": "987654321"}
]

# Charger les logs depuis un fichier JSON
def load_logs():
    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Sauvegarder les logs dans un fichier JSON
def save_logs(logs):
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file)

# Initialisation des logs
access_logs = load_logs()

@app.route('/authorized', methods=['GET'])
def get_authorized_users():
    return jsonify({"authorized_users": authorized_users})

@app.route('/access_logs', methods=['GET'])
def get_access_logs():
    return jsonify({"access_logs": access_logs})

@app.route('/log_access', methods=['POST'])
def log_access():
    data = request.json
    uid = data.get('uid')
    status = data.get('status', 'denied')
    name = data.get('name', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"name": name, "uid": uid, "status": status, "timestamp": timestamp}
    access_logs.append(log_entry)
    save_logs(access_logs)
    return jsonify({"message": "Access logged", "log_entry": log_entry}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
