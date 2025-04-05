import subprocess 
import time 
import pulsectl
from AudioData import AudioProgramm

pulse = pulsectl.Pulse('audio-stream-handler')

def _BLuetoothUnblock():                             # Aktiviert Bluetooth generell
    try:
         subprocess.run(["sudo" , "rfkill" , "unblock" , "bluetooth"])
    
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")

def _BluetoothUp():                                  # Aktiviert den Bluetooth Adapter
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "up"])
     
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}") 

def _BluetoothDown():                                # Deaktiviert den Bluetooth Adapter 
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "down"])
     
    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")

def _BluetoothScan():                                # Startet Suche nach bekannten und unbekannten Geräten
    try:
         subprocess.run(["sudo" , "hciconfig" , "hci0" , "piscan"])

    except subprocess.CalledProcessError as e:
         print(f"Fehler: {e}")  

def _BluetoothStopScan():                            # Beendet die suche nach Bluetooth Geräten
    try:
        subprocess.run(["sudo" , "hciconfig" , "hci0" , "noscan"])

    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e}") 

def BluetoothConnected():                           # Prüft ob eine Bluetooth Verbindung vorhanden ist
    try:
        OutputString = subprocess.run(["hcitool","con"], stdout = subprocess.PIPE)
            
        if len(OutputString.stdout) > 13:  #Die 13 steht für die Länge des Strings "Connections:\n"
            return True
        else:
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"Fehler: {e}")
         
         
def _BluetoothActionInTimeInterval():               # prüft ob innerhalb eines vorgegebenen Intervalls
    for i in range(1000):                           # Eine Verbindung vorhanden ist oder ein Bluetooth-
        if BluetoothConnected():                   # knopf betätigt wurde
            print("ein gerät hat sich verbunden")    
            return 1                                
        else:
            time.sleep(0.1)
    
    ShutdownRaspi()
            
def ShutdownRaspi():
    subprocess.run(["sudo","shutdown"], check = True)   # Zeitintervallüberschreitung -> Herunterfahren des Systems

#def _AudioStreamUP():
#    ConnectedDevice = pulse.sink_input_list()
#    if ConnectedDevice == []:
#        print ("Down")
#        return False
#    else:
#        print ("up")
#        return True
    
# def _BluetoothActivityCheck():
#     __Counter = 0
#     try:
#         while True:
#             if  _BluetoothConnected:
#                 time.sleep(0.5)
#                 if _AudioStreamUP():
#                     __Counter = 0
#                 else: 
#                     __Counter += 1
#                     if __Counter == 240:               # 2 min, muss noch angepasst werden
#                         print ("shutdown")
        
#             else:
#                 break
#         print("die verbindung zum gerät wurde unterbrochen")
#         _ActivateBluetooth()
    
#     except KeyboardInterrupt:
#         print("programm beendet")



def _InitializeBluetooth():                          # Initialisiert Bluetooth am anfang des Programms
    _BLuetoothUnblock()
    _BluetoothUp()

def _DisconnectAll():                                # Trennt alle vorhandenen Verbindungen 
    _BluetoothDown()
    _BluetoothUp()

def _ActivateBluetooth():                            # Programm kann nach dieser methode zwei Zustände haben: 1. Ein Gerät ist verbunden , 2. Das System fährt herunter 
    _BluetoothScan()
    if _BluetoothActionInTimeInterval() == 1:
        time.sleep(0.2)                          # ohne pause wird StopScan nicht korrekt ausgeführt 
        _BluetoothStopScan()
        #_BluetoothActivityCheck()
        AudioProgramm()
        
    elif _BluetoothActionInTimeInterval() == 2:
        _DisconnectAll()
        _ActivateBluetooth()

def BluetoothProgramm():
    _InitializeBluetooth()
    _ActivateBluetooth()

BluetoothProgramm()
    



    




     
     

