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


# This file contains the:
# Cisco DNA Center base url and will get the username and 
# password, server info from environment variables

# Update this section with the Cisco DNA Center server info,
# and user information. If server uses different HTTPS port 
# then 443 please especify, if not leave it without port number  


import os

DNAC_BASE_URL = os.getenv("DNA_CENTER_BASE_URL") or "https://sandboxdnac2.cisco.com:8080"
DNAC_USER = os.getenv("DNA_CENTER_USERNAME") or "devnetuser"
DNAC_PASS = os.getenv("DNA_CENTER_PASSWORD") or "Cisco123!"

