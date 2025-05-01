import subprocess 
import time 
from AudioData import AudioProgramm

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


def _InitializeBluetooth():                         # Initialisiert Bluetooth am anfang des Programms
    _BLuetoothUnblock()
    _BluetoothUp()


def _DisconnectAll():                               # Trennt alle vorhandenen Verbindungen 
    _BluetoothDown()
    _BluetoothUp()
         
         
def BluetoothProgramm():                           
    _InitializeBluetooth()
    _DisconnectAll()
    _BluetoothScan()
    __Starttime = time.time()
    __ShutdownTime = 15 * 60                        # 1min muss auf 15 min geändert werden
    while True:
        
        if (time.time() - __Starttime) > __ShutdownTime:
            ShutdownRaspi()

        if BluetoothConnected():
            print("ein Gerät hat sich verbunden")
            _BluetoothStopScan()
            AudioProgramm()

#       if ButtonPress():                           # zukünftige methode, die die betätigung eines knopfes an einem io pin registriert
#           _DisconnectAll()
#           _BluetoothScan()
#           __Starttime = time.time()

        time.sleep(0.1)

BluetoothProgramm()



        



    



    




     
     

