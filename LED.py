import time
import rpi_ws281x as ws

# LED configuration.
LED_CHANNEL = 0
LED_COUNT = 300             # How many LEDs to light.
LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
LED_GPIO = 18               # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT = 0              # Set to 1 to invert the LED signal, good if using NPN
#                             transistor as a 3.3V->5V level converter.  Keep at 0
#                             for a normal/non-inverted signal.

DOT_COLORS = [0x200000,     # red
              0x002000,     # green
              0x000020,     # blue
              0x20000000,   # white
              0]            # off

FrequencyBand = [2, 3, 4, 1, 5, 8, 2, 10, 3, 7]

# Initialisiere LED-Controller (Low-Level)
leds = ws.new_ws2811_t()

# Konfiguriere Kanal (hier nur Kanal 0 als Beispiel)
channel = ws.ws2811_channel_get(leds, 0)
ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)

# Initialisierung der LED-Engine
ws.ws2811_init(leds)

# Fester Farbwert für Rot (0x200000)
RED_COLOR = 0x200000

# Animation
try:
    while True:
        # Iteriere durch alle Frequenzbänder
        for i in range(10):  # 10 Frequenzbänder
            # Berechne die Start- und Endposition für das Frequenzband im LED-Streifen
            start_led = i * 10  # Beginn der Säule (jede Säule hat 10 LEDs)
            end_led = start_led + FrequencyBand[i]  # Endposition der Säule (basierend auf dem Wert)

            # Setze LEDs für dieses Frequenzband (Säule)
            for j in range(10):  # Jede Säule hat 10 LEDs
                led_index = start_led + j  # Berechne den LED-Index im Gesamtstreifen
                if led_index < end_led:  # LEDs bis zum Wert des Frequenzbandes leuchten lassen
                    ws.ws2811_led_set(channel, led_index, DOT_COLORS[0])
                else:
                    ws.ws2811_led_set(channel, led_index, DOT_COLORS[4])  # Restliche LEDs ausschalten

        # Rendere die neuen Werte auf die LEDs
        ws.ws2811_render(leds)

        # Zeitintervall von 42,6 ms
        time.sleep(0.0426)
finally:
    # Aufräumen bei Programmende
    ws.ws2811_fini(leds)
    ws.delete_ws2811_t(leds)
