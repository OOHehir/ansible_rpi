#!/usr/bin/env python3
""" Script to handle events when button pressed
    Warning: Starting the WPS process may remove any current connections """

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Error importing RPi.GPIO. Installed?")
except RuntimeError:
    print("Error need to be sudo")

import time
import os
import subprocess
import logging
import sys
from threading import Thread

BUTTON_GPIO = 22
class ButtonDriver:
    """
    Class to handle the button press event
    """
    def __init__(self, button_gpio: int):
        self.time_pressed = 0
        self.button_gpio = button_gpio
        self.wpa_state_cmnd = "wpa_cli -i wlan0 status | grep wpa_state"
        self.setup_gpio()

    def setup_gpio(self):
        """
        Setup the GPIO
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(self.button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.add_event_detect(self.button_gpio, GPIO.BOTH, callback=self.edge_callback, bouncetime=100)

    def start_wps(self):
        """
        Start WPS
        """
        logging.info("Starting WPS")
        start_cmd = "sudo wpa_cli -i wlan0 wps_pbc"
        os.system(start_cmd)
        # Wait for success, failure or timeout
        t_max = 130
        for t in range(t_max):
            result = subprocess.getoutput(self.wpa_state_cmnd)
            logging.debug("WPS status: %s, t: %d", result, t)
            if "wpa_state=COMPLETED" in result:
                logging.info("WPS success")
                # Must start DHCP
                start_dhcp_cmd = "sudo dhclient wlan0"
                os.system(start_dhcp_cmd)
                break
            if "wpa_state=FAILED" in result:
                logging.error("WPS failed")
                break
            time.sleep(1)
        else:
            logging.error("WPS timeout")

    def button_event(self, time_p_msec: float) -> None:
        """
        Handle the button press event
        """
        self.time_pressed = 0
        if time_p_msec > 3000:
            result = subprocess.getoutput(self.wpa_state_cmnd)
            logging.debug("WPS status: %s", result)
            if "wpa_state=SCANNING" in result:
                logging.warning("WPS is in progress, ignoring")
                return
            thread = Thread(target=self.start_wps)
            thread.start()
        else:
            logging.info("Button pressed for %s msec", time_p_msec)

    def edge_callback(self, channel):
        """
        Handle the edge events
        """
        logging.debug("Button: %s value: %s", channel, GPIO.input(self.button_gpio))
        if channel != self.button_gpio:
            logging.error("Wrong channel")
            return
        if GPIO.input(self.button_gpio):
            self.time_pressed = time.time() - self.time_pressed
            self.button_event(int(self.time_pressed * 1000))
        else:
            logging.debug("Button pressed")
            self.time_pressed = time.time()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Check if sudo
    if os.geteuid() != 0:
        logging.warning("Please run with sudo")
        sys.exit(1)
    button_driver = ButtonDriver(button_gpio=BUTTON_GPIO)
    while True:
        pass
