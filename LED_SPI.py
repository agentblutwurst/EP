import time
import rpi_ws281x as ws

# LED configuration.
LED_CHANNEL = 0
LED_COUNT = 100
LED_FREQ_HZ = 800000
LED_BRIGHTNESS = 255
LED_INVERT = 0

# SPI-spezifisch:
LED_GPIO = 10  # SPI MOSI
LED_GPIO_TYPE = ws.WS2811_GPIO_SPI  # Aktiviert SPI-Modus

DOT_COLORS = [
    0x200000,  # green
    0x002000,  # red
    0x000020,  # blue
    0x101010,  # white
    0x000000   # off
]

FrequencyBand1 = [2, 3, 4, 1, 5, 8, 2, 10, 3, 7]
FrequencyBand2 = [4, 1, 5, 8, 2, 10, 3, 7, 2, 3]
FrequencyBand3 = [5, 8, 2, 10, 3, 7, 2, 3, 4, 1]
FrequencyBands = [FrequencyBand1, FrequencyBand2, FrequencyBand3]

# Initialisiere LED-Controller (Low-Level)
LEDs = ws.new_ws2811_t()

# Deaktiviere beide Kanäle erst mal
for channum in range(2):
    channel = ws.ws2811_channel_get(LEDs, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)
    ws.ws2811_channel_t_strip_type_set(channel, ws.WS2811_STRIP_GRB)

# Konfiguriere Kanal 0 für SPI
channel = ws.ws2811_channel_get(LEDs, LED_CHANNEL)
ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
ws.ws2811_channel_t_strip_type_set(channel, ws.WS2811_STRIP_GRB)

# Allgemeine Einstellungen
ws.ws2811_t_freq_set(LEDs, LED_FREQ_HZ)
# KEIN ws2811_t_dmanum_set() im SPI-Modus nötig
ws.ws2811_t_gpio_type_set(LEDs, LED_GPIO_TYPE)  # <- SPI aktivieren

# Initialisierung
init_result = ws.ws2811_init(LEDs)
if init_result != 0:
    raise RuntimeError(f"ws2811_init failed with code {init_result}")

def LEDLightenUp(AmplitudeList):
    try:
        for i in range(10):  # 10 Frequenzbänder
            StartLED = i * 10
            EndLED = StartLED + AmplitudeList[i]

            for j in range(10):
                LEDIndex = StartLED + j
                if LEDIndex < EndLED:
                    ws.ws2811_led_set(channel, LEDIndex, DOT_COLORS[0])
                else:
                    ws.ws2811_led_set(channel, LEDIndex, DOT_COLORS[4])

        ws.ws2811_render(LEDs)
    finally:
        ws.ws2811_fini(LEDs)
        ws.delete_ws2811_t(LEDs)

LEDLightenUp(FrequencyBand1)