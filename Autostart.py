import subprocess
import time
import os

os.environ['PULSE_SERVER'] = "/run/user/1000/pulse/native"
time.sleep(3)
subprocess.run(["/home/EP/Documents/EP/EP/.venv/bin/python", "/home/EP/Documents/EP/EP/Bluetooth.py"])