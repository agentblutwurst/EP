import subprocess
import time

class CInquiry(object):

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
            subprocess.run(["sudo","rfkill","unblock","all"])

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

    def InitializeBluetoothConnection(self):
        if self.CheckIfBluetooth() == False:
            self.UnblockWirelessConnections()
            self.MakeDiscoverable()

        while(True):
        # weitere Abbruchbedingung hinzufügen wegen unendlicher Schleife
            if self.CheckIfBluetooth():
                self.MakeUndiscoverable()
                break


if __name__ == '__main__':
    st = time.time()

    #CInquiry.StartBluetoothService()
    #CInquiry.UnblockWirelessConnections()
    #CInquiry.EnableBluetoothService()
    #CInquiry.StartBluetoothService()
    #CInquiry.MakeDiscoverable()
    #CInquiry.CheckIfBluetooth()
    CInquiry().InitializeBluetoothConnection()

    et = time.time()

    print(et-st)