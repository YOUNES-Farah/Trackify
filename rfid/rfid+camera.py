import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import cv2

# Désactiver les avertissements
GPIO.setwarnings(False)

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)

# Pins pour le relais
RELAY_PIN = 17
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

# Pins pour le capteur ultrason
ULTRASONIC_TRIG = 5
ULTRASONIC_ECHO = 6
GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)

# Lecteur RFID
reader = SimpleMFRC522()

# Base de données des utilisateurs autorisés
AUTHORIZED_TEACHERS = ['123456789', '987654321', '462945141832'] 
AUTHORIZED_STUDENTS = ['2233445566'] 

# Fonction pour vérifier la distance avec le capteur ultrason
def check_ultrasonic():
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
    return distance

# Fonction pour ouvrir la porte
def open_door():
    print("Ouverture de la porte...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Porte fermée.")

# Fonction pour activer la caméra
def activate_camera():
    print("Activation de la caméra...")
    camera = cv2.VideoCapture(0)  # Index 0 pour la caméra par défaut
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Erreur de lecture de la caméra.")
                break
            cv2.imshow("Flux vidéo", frame)

            # Quitter la caméra si 'q' est pressé
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Fermeture de la caméra.")
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

# Fonction principale
def main():
    try:
        while True:
            print("En attente d'une personne devant la porte...")
            distance = check_ultrasonic()
            activate_camera()
            if distance < 50:  # Si une personne est détectée
                print(f"Personne détectée à {distance:.2f} cm. En attente d'une carte RFID...")

                # Lecture de la carte RFID
                id, text = reader.read()
                print(f"Carte scannée avec UID : {id}")

                # Vérification des droits d'accès
                if str(id) in AUTHORIZED_TEACHERS:
                    print("Accès autorisé : enseignant.")
                    open_door()
                      # Activer la caméra après ouverture
                elif str(id) in AUTHORIZED_STUDENTS:
                    print("Accès refusé : étudiant.")
                else:
                    print("Accès refusé : carte non reconnue.")
            else:
                print(f"Aucune personne détectée (distance : {distance:.2f} cm).")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        GPIO.cleanup()

# Exécution du programme
if __name__ == "__main__":
    main()
