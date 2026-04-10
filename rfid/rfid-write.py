import RPi.GPIO as GPIO 
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)

reader = SimpleMFRC522()
try:
	text = input ('new data : ')
	print("placer votre carte")
	reader.write(text)
	print("done")
finally:
	GPIO.cleanup()
	
