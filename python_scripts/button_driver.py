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

class ButtonDriver:
    """
    Class to handle the button press event
    """
    def __init__(self, button_gpio: int):
        self.time_pressed = 0
        self.button_gpio = button_gpio
        self.setup_gpio()

    def setup_gpio(self):
        """
        Setup the GPIO
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(True)
        GPIO.setup(self.button_gpio, GPIO.IN, pull_up_down=None)
        GPIO.add_event_detect(self.button_gpio, GPIO.FALLING, callback=self.falling_edge_callback, bouncetime=100)
        GPIO.add_event_detect(self.button_gpio, GPIO.RISING, callback=self.rising_edge_callback, bouncetime=100)

    def button_event(self, time_p: float) -> None:
        """
        Handle the button press event
        """
        if time_p > 5:
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

    def rising_edge_callback(self):
        """
        Handle the rising edge event
        """
        self.time_pressed = time.time() - self.time_pressed
        self.button_event(self.time_pressed)
        self.time_pressed = 0

    def falling_edge_callback(self):
        """
        Handle the falling edge event
        """
        self.time_pressed = time.time()

if __name__ == '__main__':
    button_driver = ButtonDriver(button_gpio=22)
    while True:
        pass
