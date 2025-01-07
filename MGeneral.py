import time

class CGeneralFunctions(object):

    def Wait(Duration):
        StartTime = time.time()  # Startzeit speichern

        while True:
            # Berechne die vergangene Zeit
            PassedTime = time.time() - StartTime

            if PassedTime >= Duration:
                break  # Schleife beenden, wenn die Dauer erreicht ist

            print(f"Verstrichene Zeit: {int(PassedTime)} Sekunden")
            time.sleep(0.1)  # Eine Zehntelsekunde warten, bevor wieder hochgezählt wird