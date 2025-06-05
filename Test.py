import RPi.GPIO as GPIO
import time

MOSFET_GATE_PIN = 17  # z. B. GPIO17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOSFET_GATE_PIN, GPIO.OUT)

for x in range(5):
    # Einschalten (MOSFET leitend → Ventil an)
    GPIO.output(MOSFET_GATE_PIN, GPIO.HIGH)
    time.sleep(0.5)

    # Ausschalten
    GPIO.output(MOSFET_GATE_PIN, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()