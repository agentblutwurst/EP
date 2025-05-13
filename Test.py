import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def KnoppGedrueckt(PinNummer):    
    Zustand = GPIO.input(PinNummer) == GPIO.LOW
    return Zustand

while True:
    print(KnoppGedrueckt(17))
    print(KnoppGedrueckt(22))
    time.sleep(0.25)