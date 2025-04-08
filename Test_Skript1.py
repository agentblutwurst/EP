import subprocess
import json

Liste = [1, 4, 2, 3, 4, 2, 2, 3, 4, 2]
ListeStr = json.dumps(Liste)

subprocess.run(["sudo", "python", "Test_Skript2.py", ListeStr])