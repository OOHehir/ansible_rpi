#!/usr/bin/python
""" Script to start WPS """
import os
import subprocess
import time
import sys

def clear_network():
    """
    Clear the network
    """
    clear_cmd = "sudo sed  -i '/network={/,$d' /etc/wpa_supplicant/wpa_supplicant-wlan0.conf"
    os.system(clear_cmd)

def start_wps():
    """
    Start WPS
    """
    start_cmd = "sudo wpa_cli -i wlan0 wps_pbc"
    os.system(start_cmd)

def check_wps_status():
    """
    Check the WPS status
    """
    check_cmd = "sudo wpa_cli -i wlan0 status | grep -Fxq wpa_state=SCANNING"
    status = subprocess.check_output(check_cmd, shell=True)
    if status == 0:
        print("WPS is in progress")
        return True
    else:
        print("WPS is not in progress")
    return False

if __name__ == '__main__':
    # Check if WPS is in progress
    if check_wps_status():
        sys.exit(0)

    # Clear the network
    clear_network()
    time.sleep(5)

    # Start
    start_wps()
