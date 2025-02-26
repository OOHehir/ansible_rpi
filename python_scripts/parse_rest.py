#!/usr/bin/env python3

# Python application to get a REST API request from a server with a JSON payload
#
# Test:
# ./parse_rest.py Battery_SOC
#
# Note: This script is expected to be located in /home/rufilla

import requests
import json
import sys

# Use these characters to identify the start and end of the data
# Easier to parse on micro-controllers
start_data = '{'
separate_data = ': '
end_data = '}'

# REST API URL
host = 'http://localhost:6345/'  # Local
#host = 'http://localhost:7345/'    # Remote - running from AWS

url =  'getCache'

if (len(sys.argv) < 2):
    print ("Please provide the key to search & optionally the test data file, e.g. ./parse_rest.py Battery_SOC")
    sys.exit()

# Function to find the key in the nested dictionary
def search_json(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from search_json(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from search_json(item, lookup_key)

# Try to find in following order:
# 1. test data file
# 2. URL
if (len(sys.argv) > 2):
    try:
        f = open(sys.argv[2])
        print ('Using test data file:', sys.argv[2])
        data = json.load(f)
    except FileNotFoundError:
        print ('Failed to open file:', sys.argv[2])
else:
    # Get the data from the REST API
    try:
        response = requests.get(host + url)
        print ('Connecting to:', host + url)
    except requests.exceptions.RequestException as e:
        print ('Failed to connect to:', host + url)
        exit(1)

    data = response.json()
    # Find every occurrence of the key in the nested dictionary & create JSON
    # Format: {"key": value}
    for item in search_json(data, sys.argv[1]):
        if type(item) == int:
            print (start_data + "\"" + sys.argv[1] + "\"" + separate_data + str(item) + end_data)
        else:
            # Add quotes to the string
            print (start_data + "\"" + sys.argv[1] + "\"" + separate_data + "\"" + str(item) + "\"" + end_data)
    exit(0)