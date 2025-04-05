import numpy as np
import plotly.express as px
from scipy import signal
import pandas as pd
import time 

# Beispiel: Erstelle ein Testsignal (z.B. Sinuswelle mit Rauschen)
fs = 1000  # Abtastrate
t = np.arange(0, 5, 1/fs)  # Zeitachse (5 Sekunden)
f1 = 50  # Frequenz 1 (50 Hz)
f2 = 150  # Frequenz 2 (150 Hz)

# Erstelle ein Signal: Kombination von zwei Sinuswellen
signal_data = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
starttime = time.time()
# Berechne die Short-Time Fourier Transform (STFT)
f, t_stft, Zxx = signal.stft(signal_data, fs, nperseg=256)
endtime = time.time()
print (endtime -starttime)
# Erstelle ein DataFrame für Plotly Express
Zxx_abs = np.abs(Zxx)  # Wir benötigen den Betrag der komplexen Werte

# Transponiere Zxx_abs, da Plotly erwartet, dass jede Zeile eine Zeit und jede Spalte eine Frequenz darstellt
df = pd.DataFrame(Zxx_abs, columns=t_stft, index=f)  # Die Zeilen sind Frequenzen, die Spalten sind Zeitpunkte

# Visualisiere das Spektrogramm mit Plotly Express
fig = px.imshow(df, 
                labels={'x': 'Zeit [s]', 'y': 'Frequenz [Hz]', 'color': 'Amplitude'},
                color_continuous_scale='Viridis', 
                title='STFT des Signals')

fig.show()