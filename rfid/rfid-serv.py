import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests

# Configuration des GPIO
RELAY_PIN = 18  # Pour la commande du relais
ULTRASONIC_TRIG = 23  # Broche TRIG du capteur ultrason
ULTRASONIC_ECHO = 24  # Broche ECHO du capteur ultrason

# Configuration du backend Flask
SERVER_URL = "http://127.0.0.1:5000"

# Initialisation des composants
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)
reader = SimpleMFRC522()

# Fonction pour envoyer des logs au backend
def send_log(uid, name, status):
    payload = {"uid": uid, "name": name, "status": status}
    try:
        response = requests.post(f"{SERVER_URL}/log_access", json=payload)
        print(f"Log envoyé: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi du log : {e}")

# Fonction pour vérifier la distance avec le capteur ultrason
def is_person_near():
    GPIO.output(ULTRASONIC_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ULTRASONIC_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ULTRASONIC_ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Distance en cm
    return distance < 50  # Personne détectée si distance < 50 cm

# Fonction principale
try:
    print("Lecture RFID en cours...")

    while True:
        if is_person_near():
            print("Personne détectée devant la porte.")

            print("Scan d'une carte RFID...")
            uid, _ = reader.read()
            uid = str(uid).strip()
            print(f"UID détecté : {uid}")

            # Vérifier l'autorisation avec le backend
            try:
                response = requests.get(f"{SERVER_URL}/authorized")
                authorized_users = response.json().get("authorized_users", [])
                user = next((u for u in authorized_users if u["uid"] == uid), None)

                if user:
                    # Utilisateur autorisé
                    print(f"Accès autorisé : {user['name']}")
                    send_log(uid, user["name"], "granted")
                    
                    # Ouvrir la porte pour les enseignants uniquement
                    if "enseignant" in user["name"].lower():
                        print("Ouverture de la porte...")
                        GPIO.output(RELAY_PIN, GPIO.HIGH)
                        time.sleep(5)  # Maintenir le relais pendant 5 secondes
                        GPIO.output(RELAY_PIN, GPIO.LOW)
                    else:
                        print("Accès refusé (non enseignant).")
                else:
                    # Utilisateur non autorisé
                    print("Accès refusé : utilisateur inconnu.")
                    send_log(uid, "Unknown", "denied")
            
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la vérification de l'accès : {e}")

        time.sleep(1)  # Pause entre les vérifications

except KeyboardInterrupt:
    print("Arrêt du système.")
finally:
    GPIO.cleanup()
