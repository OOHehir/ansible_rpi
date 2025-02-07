#!/usr/bin/env python3
# Python application to post a REST API request to a server with a JSON payload
# Sets battery level & rates

# Note: This script is expected to be located in /home/octopus

# Endpoints:
# 1 OnOff
# 2 Battery SOC
# 3 Battery Power (sent as x100's of watts)

# Test with:
# Set charge to 70% (a charge is when data is from 101 -> 200, subtract 100 to get target level):
# ./givEnergy_control.py '{"endpoint": 2, "cluster" : 8, "attribute" : "0x0", "type" : "0x20", "size" : 1, "data" : 170}'

# Set discharge to 40% (discharge is when data is from 0 -> 100):
# ./givEnergy_control.py '{"endpoint": 2, "cluster" : 8, "attribute" : "0x0", "type" : "0x20", "size" : 1, "data" : 40}'

# Set rate to 300W (uses endpoint 3, retained on RPi & used when charge/ discharge is set):
# ./givEnergy_control.py '{"endpoint": 3, "cluster" : 8, "attribute" : "0x0", "type" : "0x20", "size" : 1, "data" : 3}'

# Set rate to 0W, used to stop charging/ discharging:
# ./givEnergy_control.py '{"endpoint": 3, "cluster" : 8, "attribute" : "0x0", "type" : "0x20", "size" : 1, "data" : 0}'

# Check results:
# curl -s localhost:6345/runAll | grep "Charge_Power\|Discharge_Power\|battery_percent\|Eco_Mode"

import requests
import sys
import json
from time import sleep
from datetime import datetime, timedelta

# REST API URL
host = 'http://localhost:6345/'     # Local
#host = 'http://localhost:7345/'    # Remote - running from AWS

log_file = 'givEnergy_log.txt'

BATTERY_DEFAULT_RATE = 300

battery_mode_urls =  [  'enableChargeSchedule',
                        'enableDischargeSchedule',
                        ]

charge_urls =  ['enableDischarge',
                'setBatteryMode',
                'setChargeRate',
                'setChargeSlot1',
                'enableChargeTarget',
                'enableChargeSchedule',
                ]

discharge_urls =  [ 'setBatteryMode',
                    'enableChargeSchedule',
                    'setDischargeSlot1',
                    'setDischargeRate',
                    'enableDischargeSchedule',
                ]

def check_input(input: list) -> dict:
    '''
    Check the input JSON
    '''
    if (len(input) < 2):
        print ('Usage: givEnergy_control.py <JSON> , e.g. givEnergy_control.py \'{"endpoint": 3, "cluster" : 8, "attribute" : "0x0", "type" : "0x20", "size" : 1, "data" : 255}\'')
        sys.exit()
    else:
        try:
            json_dict = json.loads(input[1])
        except ValueError as e:
            print("Invalid JSON")
            sys.exit()
        print("JSON received: " + json.dumps(json_dict, indent=4))
        return json_dict

def get_time_str() -> str:
    '''
    Time format for log file
    '''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_to_file(log_str: str) -> None:
    '''
    Log a string to file
    '''
    try:
        f = open(log_file, 'a')
    except FileNotFoundError:
        print ('Failed to open file:', log_file)
        sys.exit()
    f.write(get_time_str() + " " + log_str  + "\n")

def set_battery_mode_payload():
    payload = [ '{"state":"disable"}',
                '{"state":"disable"}',
                ]
    return payload, battery_mode_urls

def set_battery_payload(json_dict: dict) -> tuple[list[str], list[str]]:
    '''
    Set battery level
    This function sets the battery level & stores to file for later use
    Note the battery level is sent as a percentage
    The battery rate is retrieved from a file or uses a default value
    '''
    # Try to get the rate from the file
    try:
        with open('givEnergy_data.json', 'r') as f:
            data = json.load(f)
            rate = data['rate']
    except FileNotFoundError:
        print ('Failed to open file: givEnergy_data.json, using default rate')
        rate = BATTERY_DEFAULT_RATE

    now = datetime.now()
    hour_ago = (now - timedelta(hours=1)).strftime("%H:%M")
    hour_ahead = (now + timedelta(hours=1)).strftime("%H:%M")

    # Charge or discharge?
    # 0 -> 100 discharge
    # 100 -> 200 charge (need to subtract 100)
    if json_dict['data'] >= 98 and json_dict['data'] <= 100:
        print("Can't discharge to " + format(json_dict['data']))
        log_to_file("Can't discharge to " + format(json_dict['data']))
        exit()
    elif json_dict['data'] >= 0 and json_dict['data'] < 98:
        # Discharge
        payload = [ '{"mode":"Timed Export"}',
                    '{"state":"disable"}',
                    '{"start": "' + format(hour_ago) + '", "finish": "' + format(hour_ahead) + '", "dischargeToPercent":"' + format(json_dict['data']) + '"}',
                    '{"dischargeRate":"' + format(rate) + '"}',
                    '{"state":"enable"}',
                    ]
        log_to_file("Payload: " + format(payload))
        return payload, discharge_urls
    elif json_dict['data'] > 100 and json_dict['data'] <= 103:
        # Note: need to correct the level!
        level = json_dict['data'] - 100
        print("Can't charge to " + format(level))
        log_to_file( "Can't charge to " + format(level))
        exit()
    elif json_dict['data'] > 103 and json_dict['data'] <= 200:
        # Charge
        # Note: need to correct the level!
        level = json_dict['data'] - 100
        payload = [ '{"state":"disable"}',
                    '{"state":"disable"}',
                    '{"chargeRate":"' + format(rate) + '"}',
                    '{"start": "' + format(hour_ago) + '", "finish": "' + format(hour_ahead) + '", "chargeToPercent":"' + format(level) + '"}',
                    '{"state":"enable"}',
                    '{"state":"enable"}']
        log_to_file("Sending: " + format(payload))
        return payload, charge_urls
    else:
        print("Level not found/ outside range")
        log_to_file( "Level not found/ outside range")
        exit()

def send_battery_payload(payload: list, urls: list) -> None:
    '''
    Sends the constructed list via http request
    '''
    for (url, _payload) in zip(urls, payload):
        print("Sending: " + host + url + " " + _payload)
        log_to_file("Sending: " + host + url +  " " + _payload)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            response = requests.post(host + url, data=_payload, headers=headers)
            if not response.ok:
                print("FAIL")
                log_to_file("Response: FAIL")
                # print(response.text) <- No useful information
                # print(response.status_code)
            else:
                print("Response: OK")
                log_to_file("Response: OK")
        except requests.exceptions.RequestException as e:
            print("Response: FAIL")
            log_to_file("Response: FAIL")
        sleep(1)

def set_battery_rate(data: dict) -> None:
    '''
    Set battery rate
    Note: This function corrects the rate & stores to file for later use
    '''
    rate = json_dict['data'] *100
    if rate == 0:
        # Set battery mode to ECO & don't store the value
        payload, urls = set_battery_mode_payload()
        send_battery_payload(payload, urls)
    elif rate > 0 and rate < 10000:
        # Limit to 10kW
        data = {"time" : "'" + get_time_str() + "'", "rate": rate}
        with open('givEnergy_data.json', 'w') as f:
            json.dump(data, f)
        log_to_file("Stored battery rate " + format(rate))
    else:
        print("Invalid data value")
        sys.exit()

if __name__ == "__main__":
    json_dict = check_input(sys.argv)
    log_to_file("Input: " + " " + json.dumps(json_dict))

    if json_dict['endpoint'] == 2:
        # Set battery level
        payload, urls = set_battery_payload(json_dict)
        send_battery_payload(payload, urls)
    elif json_dict['endpoint'] == 3 and json_dict["type"] == "0x20":
        # Note: Should really check attribute also but seems to be always 0x0 from ESP32
        # Set battery power
        set_battery_rate(json_dict)
    sys.exit()
