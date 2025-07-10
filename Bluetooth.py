import subprocess 
import time 
from AudioData import AudioProgramm
import RPi.GPIO as GPIO

Status = 0
MOSFET_GATE_PIN0 = 5
MOSFET_GATE_PIN1 = 6

def ShutdownRaspi():
    subprocess.call(["sudo","shutdown","now"])

def _BLuetoothUnblock():                            # Aktiviert Bluetooth generell
    try:
         subprocess.run(["sudo" , "rfkill" , "unblock" , "bluetooth"])
    
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")

def _BluetoothUp():                                 # Aktiviert den Bluetooth Adapter
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "up"])
     
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}") 

def _BluetoothDown():                               # Deaktiviert den Bluetooth Adapter 
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "down"])
     
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")

def _BluetoothScan():                               # Startet Suche nach bekannten und unbekannten Geräten
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "piscan"])

    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")  

def _BluetoothStopScan():                           # Beendet die suche nach Bluetooth Geräten
    try:
        subprocess.run(["sudo" , "hciconfig" , "hci0" , "noscan"])

    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e}") 

def BluetoothConnected():                           # Prüft ob eine Bluetooth Verbindung vorhanden ist
    try:
        __OutputString = subprocess.run(["hcitool","con"], stdout = subprocess.PIPE)
            
        if len(__OutputString.stdout) > 13:         #Die 13 steht für die Länge des Strings "Connections:\n"
            return True
        else:
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e}")

def _InitGPIOs():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)                              #Ventile
    GPIO.setup(MOSFET_GATE_PIN0, GPIO.OUT)
    GPIO.setup(MOSFET_GATE_PIN1, GPIO.OUT)
    GPIO.setup(17, GPIO.IN , pull_up_down=GPIO.PUD_UP) #Bluetooth Knopf
    GPIO.setup(22, GPIO.IN , pull_up_down=GPIO.PUD_UP) #Leiser Knopf
    GPIO.setup(27, GPIO.IN , pull_up_down=GPIO.PUD_UP) #Lauter Knopf
    GPIO.setup(23, GPIO.OUT) #Leuchte Bluetooth Knopf
    GPIO.setup(24, GPIO.OUT) #Leuchte Leiser Knopf
    GPIO.setup(25, GPIO.OUT) #Leuchte Lauter Knopf


def ButtonBlink():
    global Status
    if Status == 0:
        GPIO.output(23, GPIO.HIGH)
        Status = 1
        return

    if Status == 1:
        GPIO.output(23, GPIO.LOW)
        Status = 0
        return


def _InitializeBluetooth():                         # Initialisiert Bluetooth am anfang des Programms
    _BLuetoothUnblock()
    _BluetoothUp()


def _DisconnectAll():                               # Trennt alle vorhandenen Verbindungen 
    _BluetoothDown()
    _BluetoothUp()
         
         
def BluetoothProgramm():  
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)                         
    _InitializeBluetooth()
    _DisconnectAll()
    _BluetoothScan()
    __StarttimeShutdown = time.time()
    __StarttimeBlink = time.time()
    __ShutdownTime = 15 * 60                        # 1min muss auf 15 min geändert werden
    __BlinkTime = 0.75 * 1
    while True:
        
        if (time.time() - __StarttimeShutdown) > __ShutdownTime:
            ShutdownRaspi()

        if (time.time() - __StarttimeBlink) > __BlinkTime:
            ButtonBlink()
            __StarttimeBlink = time.time()

        if BluetoothConnected():
            print("ein Gerät hat sich verbunden")
            _BluetoothStopScan()
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(25, GPIO.HIGH)
            AudioProgramm()

        time.sleep(0.1)

_InitGPIOs()
BluetoothProgramm()