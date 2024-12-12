import bluetooth
import subprocess
import time

class CInquiry(object):

    def __init__(self):
        pass

    """def SearchDevices():
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("Found {} devices.".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))"""

    def EnableBluetoothService():
        try:
            subprocess.run(["sudo","systemctl","enable","bluetooth"], check = True)
            print("Blootooth aktiviert")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def StartBluetoothService():
        try:
            subprocess.run(["sudo","systemctl","start","bluetooth"], check = True)
            print("Blootooth gestartet")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def StopBluetoothService():
        try:
            subprocess.run(["sudo","systemctl","stop","bluetooth"], check = True)
            print("Blootooth gestopt")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def MakeDiscoverable():
        try:
            subprocess.run(["bluetoothctl"], input="power on\nagent on\ndiscoverable on".encode(), text=False)

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def MakeUndiscoverable():
        try:
            subprocess.run(["bluetoothctl"], input="power on\nagent on\ndiscoverable off".encode(), text=False)

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def UnblockWirelessConnections():
        try:
            subprocess.run(["sudo","rfkill","unblock","all"])

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")
            

if __name__ == '__main__':
    st = time.time()

    #CInquiry.StartBluetoothService()
    CInquiry.UnblockWirelessConnections()
    CInquiry.EnableBluetoothService()
    CInquiry.StartBluetoothService()
    CInquiry.MakeDiscoverable()
    

    et = time.time()

    print(et-st)
    #if :
        #CInquiry.MakeUndiscoverable()