#!/usr/bin/env python3
""" Script to drive WS2812 led """

import time
import subprocess
import sys

try:
    from rpi_ws281x import ws, Color, Adafruit_NeoPixel
except ImportError:
    print('WS2812 library not found')
    # Next time Ansible runs, it will install the library
    # Let systemctl restart the service
    sys.exit(1)

LED_COUNT = 1        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_BRIGHTNESS = 30   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # 0 or 1
LED_STRIP = ws.WS2811_STRIP_GRB

NETWORK_CONNECTED = False
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)

def check_internet_connection():
    """
    Check if the internet connection is available
    """
    global NETWORK_CONNECTED
    while True:
        try:
            subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
            NETWORK_CONNECTED = True
        except subprocess.CalledProcessError:
            NETWORK_CONNECTED = False
        time.sleep(10)

if __name__ == '__main__':
    strip1 = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                               LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                               LED_CHANNEL, LED_STRIP)

    strip1.begin()
    blackout(strip1)
    # Start the thread to check the internet connection
    subprocess.run(check_internet_connection(), check=False)

    while True:
        for _ in range(2):
            if NETWORK_CONNECTED:
                # Set the LED color to green
                strip1.setPixelColor([0], GREEN)
                time.sleep(0.1)
            else:
                # Set the LED color to red
                strip1.setPixelColor([0], RED)
                time.sleep(0.1)
            strip1.setPixelColor([0], BLACK)
            time.sleep(0.1)
        time.sleep(0.8)
