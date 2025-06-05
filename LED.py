import time
import json
import sys
import rpi_ws281x as ws


# ListStr = sys.argv[1]
# List = json.loads(ListStr)

# LED configuration.
LED_CHANNEL = 0
LED_COUNT = 100             # How many LEDs to light.
LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
LED_GPIO = 12               # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT = 0              # Set to 1 to invert the LED signal, good if using NPN
#                             transistor as a 3.3V->5V level converter.  Keep at 0
#                             for a normal/non-inverted signal.

DOT_COLORS = [0x002000,     # red
              0x102000,     # orange
              0x202000,     # yellow
              0x200c00,     # green with a lil bit of yellow
              0x200000,     # green
              0x200008,     # light green
              0x180020,     # cyan
              0x000020,     # blue
              0x00101c,     # violet
              0x002014,     # pink
              0x0]            # off

#FrequencyBand1 = [2, 3, 4, 1, 5, 8, 2, 10, 3, 7]
#FrequencyBand2 = [4, 1, 5, 8, 2, 10, 3, 7, 2, 3]
#FrequencyBand3 = [5, 8, 2, 10, 3, 7, 2, 3, 4, 1]

#FrequencyBands = [FrequencyBand1,
#                FrequencyBand2,
#                FrequencyBand3]

# Initialisiere LED-Controller (Low-Level)
LEDs = ws.new_ws2811_t()

for channum in range(2):
    channel = ws.ws2811_channel_get(LEDs, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)

# Konfiguriere Kanal (hier nur Kanal 0 als Beispiel)
channel = ws.ws2811_channel_get(LEDs, LED_CHANNEL)

ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)

ws.ws2811_t_freq_set(LEDs, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(LEDs, LED_DMA_NUM)

# Initialisierung der LED-Engine
ws.ws2811_init(LEDs)


# def LEDLightenUp(AmplitudeList): ///////
    # Animation
def funk(List):
    # Iteriere durch alle Frequenzbänder
    for i in range(10):  # 10 Frequenzbänder
        # Berechne die Start- und Endposition für das Frequenzband im LED-Streifen
        StartLED = i * 8  # Beginn der Säule (jede Säule hat 8 LEDs)
        # print(i)
        # print(List[i])
        EndLED = StartLED + List[i]  # AmplitudeList ///////# Endposition der Säule (basierend auf dem Wert)

        # Setze LEDs für dieses Frequenzband (Säule)
        for j in range(8):  # Jede Säule hat 8 LEDs
            LEDIndex = StartLED + j  # Berechne den LED-Index im Gesamtstreifen
            if LEDIndex < EndLED:  # LEDs bis zum Wert des Frequenzbandes leuchten lassen
                ws.ws2811_led_set(channel, LEDIndex, DOT_COLORS[i])
            else:
                ws.ws2811_led_set(channel, LEDIndex, DOT_COLORS[10])  # Restliche LEDs ausschalten

        # Rendere die neuen Werte auf die LEDs
        ws.ws2811_render(LEDs)

        # Zeitintervall von 42,6 ms
        # time.sleep(1)
        # time.sleep(0.0426)
    
        

if __name__ == "__main__":
    try:
        for Line in sys.stdin:
            if not Line.strip():
                continue
            List = json.loads(Line)
            funk(List)
    except KeyboardInterrupt:
        pass
    finally:
        # Aufräumen bei Programmende
        ws.ws2811_fini(LEDs)
        ws.delete_ws2811_t(LEDs)