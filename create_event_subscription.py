#!/usr/bin/env python
"""

Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
__author__ = "Luis Kopti Software Architect"
__email__ = "lkopti@cisco.com"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from os import stat_result
from telnetlib import STATUS
from textwrap import indent
import requests
import json
import urllib3
import time
import sys
import xlwt
import xlrd

from xlwt import Workbook
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from config import DNAC_BASE_URL,DNAC_USER,DNAC_PASS

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access Cisco DNA Center
    Call to Cisco DNA Center - /api/system/v1/auth/login
    :param dnac_auth - Cisco DNA Center Basic Auth string
    :return Cisco DNA Center Token
    """
    url = DNAC_BASE_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    response_json = response.json()
    dnac_jwt_token = response_json['Token']
    return dnac_jwt_token

def read_excel(list_id_filename):
    """
    This function will read the list of events to be applied from 
    the local filesystem 
    :param ist_id_filename: List with events to be applied
    :return: json dictionary of EventIds 
    """
    workbook = xlrd.open_workbook(list_id_filename)

    sheet1 = workbook.sheet_by_index(0)

    event_dict = []

    for rowNumber in range(sheet1.nrows):
        row = sheet1.row_values(rowNumber)
        event_dict += row

    return event_dict

def create_event_subscription(subscription_name, description, instance_id, event_list_id, dnac_jwt_token):
    """
    This function will create the event subscription and return status code.
    :param subscription_name: the event subscription name given
    :param description: description for the event subscription to be created
    :param instance_id: the instance id retrieved from previous created Webhook
    :param event_list_id: the event list to be applied.
    :param dnac_jwt_token: Cisco DNA Center token
    :return: response
    """

    # create the event subscription
    payload = [
        {
            "name": subscription_name,
            "description": description,
            "subscriptionEndpoints": [
                {
                    "instanceId": instance_id,
                    "subscriptionDetails": {
                        "connectorType": "REST"
                        }
                }
            ],
            "filter": {
                "eventIds": event_list_id
            }
        }
    ]
    url = DNAC_BASE_URL + '/dna/intent/api/v1/event/subscription/rest'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    return response_json

def main(subscription_name, description, instance_id, list_id_filename):
    """
    This sample script will execute one CLI command {command} on the device {device_hostname}:
     - obtain the Cisco DNA Center auth token
     - read the list of event to be aplied and generate a json dict output
     - call dnac to crete the event subscription
    :param subscription_name: the event subscription name given
    :param description: description for the event subscription to be created
    :param instance_id: the instance id retrieved from previous created Webhook
    :param list_id_filename: the file name of excel sheet with event list to be applied.
    """
    print('\nApplication started')

    # obtain the Cisco DNA Center Auth Token
    print('\nGet DNAC Token...')
    dnac_token = get_dnac_jwt_token(DNAC_AUTH)

    # read the Event list
    print('\nReading list of events...')
    event_list_id = read_excel(list_id_filename)

    # call DNAC to create the event subscription
    print('\nCreating Event subscriptiomn list...')
    status_result = create_event_subscription(subscription_name, description, instance_id, event_list_id, dnac_token)
    print("Event Created\n" + str(status_result))

    print('\nEnd of Application Run\n')

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))


