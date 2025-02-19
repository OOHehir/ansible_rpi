#!/usr/bin/env python3
""" Script to handle events when button pressed """

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Error importing RPi.GPIO. Installed?")
except RuntimeError:
    print("Error need to be sudo")

import time
import os
import RPi.GPIO as GPIO

time_pressed = 0
BUTTON_GPIO = 22

def button_event(time_pressed: float) -> None:
    """
    Handle the button press event
    """
    if time_pressed >5:
        # Start WPS
        print("Starting WPS")
        cm = "sudo wpa_cli -i wlan0 wps_pbc"
        os.system(cm)
    if time_pressed > 3:
        print("Button pressed for {} seconds".format(time_pressed))

    time_pressed = 0


def rising_edge_callback():
    """
    Handle the rising edge event
    """
    global time_pressed
    time_pressed = time.time() - time_pressed
    button_event(time_pressed)

def falling_edge_callback():
    """
    Handle the falling edge event
    """
    global time_pressed
    time_pressed = time.time()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(True)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=None)

    GPIO.event_detected(BUTTON_GPIO)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=falling_edge_callback(), bouncetime=100)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=rising_edge_callback(), bouncetime=100)

    while True:

    GPIO.cleanup()