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
import subprocess
import RPi.GPIO as GPIO

time_pressed = 0
BUTTON_GPIO = 22

def button_event(time_p: float) -> None:
    """
    Handle the button press event
    """
    if time_p >5:
        check_cmd = "sudo wpa_cli -i wlan0 status | grep -Fxq wpa_state=SCANNING"
        status = subprocess.check_output(check_cmd, shell=True)
        if status == 0:
            print("WPS is in progress")
            return

        # Clear the network
        clear_cmd = "sudo sed  -i '/network={/,$d' /etc/wpa_supplicant/wpa_supplicant-wlan0.conf"
        os.system(clear_cmd)
        time.sleep(5)

        # Start WPS
        print("Starting WPS")
        start_cmd = "sudo wpa_cli -i wlan0 wps_pbc"
        os.system(start_cmd)

    if time_p > 3:
        print(f"Button pressed for {time_p} seconds")

def rising_edge_callback():
    """
    Handle the rising edge event
    """
    global time_pressed
    time_pressed = time.time() - time_pressed
    button_event(time_pressed)
    time_pressed = 0

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
        time.sleep(1)

    # Unreachable code
    GPIO.cleanup()
