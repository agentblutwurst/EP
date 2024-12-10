import bluetooth
import subprocess

class CInquiry(object):

    def __init__(self):
        pass

    def SearchDevices():
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("Found {} devices.".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))

    def StartBluetoothService():
        try:
            subprocess.run(["sudo","systemctl","enable","bluetooth"], check = True)
            print("Blootooth aktiviert")

        except subprocess.CalledProcessError as e:
            print(f"fehler: {e}")

    def MakeDiscoverable():
        input_data =  "power on\nagent on\ndiscoverable on"
        try:
            subprocess.run(["bluetoothctl"], input="power on\nagent on\ndiscoverable on".encode(), text=False)

        except subprocess.CalledProcessError as e:
            print(f"fehler: {e}")
            

if __name__ == '__main__':
    #CInquiry.StartBluetoothService()
    CInquiry.MakeDiscoverable()