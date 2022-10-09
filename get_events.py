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

from textwrap import indent
import requests
import json
import urllib3
import time
import sys
import xlwt

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

def get_event_id_list(dnac_jwt_token):
    """
    This function will get all the event ids and details 
    :param dnac_jwt_token: Cisco DNA Center token
    :return: list of events 
    """
    url = DNAC_BASE_URL + '/dna/system/api/v1/event/artifact?limit=300'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    return response_json

def write_excel(event_id_list):
    """
    This function will write the results from all the event ids and details
    to a excel sheet in local filesystem 
    :param event_id_list: List with All returned event ids
    :return: NA 
    """
    wb = Workbook()
    sheet1 = wb.add_sheet('Events')
    style = xlwt.easyxf('font: bold 1')
    sheet1.write(0, 0, 'Event ID', style)
    sheet1.write(0, 1, 'Name', style)
    sheet1.write(0, 2, 'Description', style)
    sheet1.write(0, 3, 'Type', style)
    sheet1.write(0, 4, 'Category', style)
    sheet1.write(0, 5, 'Severity', style)

    row = 1
    col = 0
    for i in event_id_list:
        sheet1.write(row, col, i['eventPayload']['eventId'])
        sheet1.write(row, col + 1, i['name'])
        sheet1.write(row, col + 2, i['description'])
        sheet1.write(row, col + 3, i['eventPayload']['type'])
        sheet1.write(row, col + 4, i['eventPayload']['category'])
        sheet1.write(row, col + 5, i['eventPayload']['severity'])
        row += 1

    wb.save('Events.xls')
    print('\nDone!')

if __name__ == "__main__":
    print('\nApplication started')

    # obtain the Cisco DNA Center Auth Token
    print('\nGet DNAC Token...')
    dnac_token = get_dnac_jwt_token(DNAC_AUTH)
    
    #obtain the list of Events available.
    print('\nGetting Event List')
    event_id_list = get_event_id_list(dnac_token)

    #obtain excel sheet
    print('\nWriting excel sheet')
    write_excel(event_id_list)

