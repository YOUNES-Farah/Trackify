import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

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
    # Envoi d'un signal
    GPIO.output(ULTRASONIC_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIG, False)

    # Mesure du temps de retour
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ULTRASONIC_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ULTRASONIC_ECHO) == 1:
        stop_time = time.time()

    # Calcul de la distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Distance en cm
    return distance

# Fonction pour ouvrir la porte
def open_door():
    print("Ouverture de la porte...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Active le relais pour ouvrir la porte

# Fonction pour ouvrir la porte
def close_door():
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Désactiver le relais pour fermer la porte
    print("Porte fermée.")

# Fonction principale
def main():
    try:
        while True:
            print("En attente d'une personne devant la porte...")
            # Vérifie la présence d'une personne avec le capteur ultrason
            distance = check_ultrasonic()
            if distance < 50:  # Si une personne est détectée à moins de 50 cm
                print(f"Personne détectée à {distance:.2f} cm. En attente d'une carte RFID...")

                # Lecture de la carte RFID
                id, text = reader.read()
                print(f"Carte scannée avec UID : {id}")

                # Vérification des droits d'accès
                if str(id) in AUTHORIZED_TEACHERS:
                    print("Accès autorisé : enseignant.")
                    open_door()
                    time.sleep(5)
                    if str(id) in AUTHORIZED_TEACHERS:
                        close_door()
                elif str(id) in AUTHORIZED_STUDENTS:
                    print("Accès refusé : étudiant.")
                else:
                    print("Accès refusé : carte non reconnue.")
            else:
                print(f"Aucune personne détectée (distance : {distance:.2f} cm).")
            time.sleep(1)  # Pause pour éviter une surcharge de la boucle
    except KeyboardInterrupt:
        print("Arrêt du programme.")
    finally:
        GPIO.cleanup()  # Nettoyage des GPIO à la fin

# Exécution du programme
if __name__ == "__main__":
    main()
