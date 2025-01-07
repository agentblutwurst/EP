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

class CBluetoothModules(object):
    def InitializeBluetoothConnection():
        if not CBluetoothFuctions.CheckIfBluetooth():
            CBluetoothFuctions.UnblockWirelessConnections()
            CBluetoothFuctions.MakeDiscoverable()

        for i in 100:
        # weitere Abbruchbedingung hinzufügen wegen unendlicher Schleife
            if CBluetoothFuctions.CheckIfBluetooth():
                CBluetoothFuctions.MakeUndiscoverable()
                break

            time.sleep(0.1)

        subprocess.run(["sudo","shutdown"], check = True)



if __name__ == '__main__':
    st = time.time()

    CBluetoothModules().InitializeBluetoothConnection()

    et = time.time()

    print(et-st)