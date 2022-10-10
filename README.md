# DNAC_Events
# ATT Conexus handle DNAC events subscription to Matrix


This series of Python scripts can be used to extract a list of Events detail from DNA Center and manage subscriptions.

**Cisco Products & Services:**

- Cisco DNA Center
- Cisco Matrix

**Tools & Frameworks:**

- Python environment

**Usage**

This sample script will get a list of events from DNA Center using the API:

 - obtain the Cisco DNA Center auth token
 - retrieve the list of events Ids and details
 - write down the output to a excel sheet file
 
Run the get events script using the command:

$ python get_events.py

**_NOTE_** Make sure to export the os env variables with DNAC base url, usertname and password before run the script.


Example:

$ export DNA_CENTER_BASE_URL=https://{dnac_Ipaddress_or_hostname}

$ export DNA_CENTER_USERNAME={usernamne}

$ export DNA_CENTER_PASSWORD={password} 

$ python get_events.py 

**Sample Output**

Application started

Get DNAC Token...

Getting Event List

Writing excel sheet

Done!

Run the create_event_subscription script using the command:

$ python create_event_subscription.py

Example:

$ python create_event_subscription.py "Name for the Event Subscription" "Description for the Event Subscription" "63613c37-9513-44d5-8476-54a953172c08" Events_list.xls

**Sample Output**

Run the get_event_subscription_details script using the command:

$ python get_event_subscription_details.py

Example:

$ python get_event_subscription_details.py "Name for the Event Subscription"

**Sample Output**

**License**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
