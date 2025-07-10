import RPi.GPIO as GPIO
import time

# MOSFET_GATE_PIN = 5  # z. B. GPIO17 (Pin 11)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(MOSFET_GATE_PIN, GPIO.OUT)

# for x in range(5):
#     # Einschalten (MOSFET leitend → Ventil an)
#     GPIO.output(MOSFET_GATE_PIN, GPIO.HIGH)
#     time.sleep(0.5)

#     # Ausschalten
#     GPIO.output(MOSFET_GATE_PIN, GPIO.LOW)
#     time.sleep(1)

# GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN , pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.OUT)

while(True):
    if GPIO.input(17) == GPIO.LOW:
        GPIO.output(23, GPIO.HIGH)
        print("True")

    else:
        GPIO.output(23, GPIO.LOW)
        print("false")

    time.sleep(0.2)