import subprocess
import time
import MGeneral

class CBluetoothFuctions(object):

    def __init__(self):
        pass

    def EnableBluetoothService(self):
        try:
            subprocess.run(["sudo","systemctl","enable","bluetooth"], check = True)
            print("Blootooth aktiviert")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def StartBluetoothService(self):
        try:
            subprocess.run(["sudo","systemctl","start","bluetooth"], check = True)
            print("Blootooth gestartet")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def StopBluetoothService(self):
        try:
            subprocess.run(["sudo","systemctl","stop","bluetooth"], check = True)
            print("Blootooth gestopt")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def MakeDiscoverable(self):
        try:
            subprocess.run(["bluetoothctl"], input="power on\nagent on\ndiscoverable on".encode(), text=False)

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def MakeUndiscoverable(self):
        try:
            subprocess.run(["bluetoothctl"], input="power on\nagent on\ndiscoverable off".encode(), text=False)

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def UnblockWirelessConnections(self):
        try:
            subprocess.run(["sudo","rfkill","unblock","bluetooth"])

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def BlockWirelessConnections(self):
        try:
            subprocess.run(["sudo","rfkill","block","bluetooth"])

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def CheckIfBluetooth(self):
        try:
            OutputString = subprocess.run(["hcitool","con"], stdout = subprocess.PIPE)
            
            if len(OutputString.stdout) > 13:  #Die 13 steht für die Länge des Strings "Connections:\n"
                return True
            else:
                return False

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def ForbidConnections(self):
        try:
            subprocess.run(["sudo","hciconfig","hci0","noscan"])

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def AllowConnections(self):
        try:
            subprocess.run([])

class CBluetoothModule(object):

    def __init__(self):
        self.__ACheckIfBluetooth = CBluetoothFuctions().CheckIfBluetooth()
        self.__AUnblockWirelessConnections = CBluetoothFuctions().UnblockWirelessConnections()
        self.__AMakeDiscoverable = CBluetoothFuctions().MakeDiscoverable()
        self.__AMakeUndiscoverable = CBluetoothFuctions().MakeUndiscoverable()
    
    def InitializeBluetoothConnection(self):
        while True:
            if not self.__ACheckIfBluetooth:
                self.__AUnblockWirelessConnections
                self.__AMakeDiscoverable

            for i in range(1200):
            # weitere Abbruchbedingung hinzufügen wegen unendlicher Schleife, CHECK
                if self.__ACheckIfBluetooth:
                    self.__AMakeUndiscoverable

                    break

                time.sleep(0.1)
            


            break

        subprocess.run(["sudo","shutdown"], check = True)



if __name__ == '__main__':
    st = time.time()

    CBluetoothModule().InitializeBluetoothConnection()

    et = time.time()

    print(et-st)