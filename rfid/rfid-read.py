from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

reader = SimpleMFRC522()

try:
    while True:
        print("Placer votre carte ...")
        id, text = reader.read()
        print("id : ")
        print(id)
        print(text)
finally : 
	GPIO.cleanup()
