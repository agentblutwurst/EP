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

    """def CheckBluetoothConnection():
        try:
            result = subprocess.run(["hciconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if "UP RUNNING\n" in result.stdout:
                print(result.stdout, " , passt")

            else:
                print(result.stdout, " , funzt net")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")"""

    def CheckIfBluetooth():
        try:
            subprocess.run(["bluetoothctl"], input="show".encode(), text=False)

            print(" , passt")

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

    def CheckIfBluetooth0():
        try:
            result = subprocess.run(["bluetoothctl"], input="power on\nagent on".encode(), text=False, stdout=subprocess.PIPE)
            word_to_count = "[bluetooth]"
            word_count = str(result.stdout).count(word_to_count)

            print(result.stdout)
            print(word_count)

        except subprocess.CalledProcessError as e:
            print(f"Fehler: {e}")

            

if __name__ == '__main__':
    st = time.time()

    #CInquiry.StartBluetoothService()
    #CInquiry.UnblockWirelessConnections()
    #CInquiry.EnableBluetoothService()
    #CInquiry.StartBluetoothService()
    #CInquiry.MakeDiscoverable()
    #CInquiry.CheckIfBluetooth()
    CInquiry.CheckIfBluetooth0()
    

    et = time.time()

    print(et-st)
    #if :
        #CInquiry.MakeUndiscoverable()