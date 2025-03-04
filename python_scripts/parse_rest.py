#!/usr/bin/env python3
''' Application to get a REST API request from a server with a JSON payload
    ./parse_rest.py Battery_SOC
    Note: This script is expected to be located in /home/octopus

'''
import json
import sys
import requests

# Use these characters to identify the start and end of the data
# Easier to parse on micro-controllers
START_DATA = '{'
SEPARATE_DATA = ': '
END_DATA = '}'

# REST API URL
host = 'http://localhost:6345/'  # Local
#host = 'http://localhost:7345/'    # Remote - running from AWS

url =  'getCache'

if len(sys.argv) < 2:
    print ("Provide the key to search & optionally the test data file, e.g. ./parse_rest.py Battery_SOC")
    sys.exit(1)

def search_json(json_input, lookup_key):
    '''Function to find the key in the nested dictionary'''
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from search_json(v, lookup_key)
    elif isinstance(json_input, list):
        for item_l in json_input:
            yield from search_json(item_l, lookup_key)

# Try to find in following order:
# 1. test data file
# 2. URL
if len(sys.argv) > 2:
    try:
        with open(sys.argv[2], encoding="utf-8") as f:
            print ('Using test data file:', sys.argv[2])
            data = json.load(f)
    except FileNotFoundError:
        print ('Failed to open file:', sys.argv[2])
else:
    # Get the data from the REST API
    try:
        response = requests.get(host + url, timeout=20)
        print ('Connecting to:', host + url)
    except requests.exceptions.RequestException as e:
        print ('Failed to connect to:', host + url)
        sys.exit(1)

    data = response.json()
    # Find every occurrence of the key in the nested dictionary & create JSON
    # Format: {"key": value}
    for item in search_json(data, sys.argv[1]):
        if isinstance(item, int):
            print (START_DATA + "\"" + sys.argv[1] + "\"" + SEPARATE_DATA + str(item) + END_DATA)
        else:
            # Add quotes to the string
            print (START_DATA + "\"" + sys.argv[1] + "\"" + SEPARATE_DATA + "\"" + str(item) + "\"" + END_DATA)
    sys.exit(0)
