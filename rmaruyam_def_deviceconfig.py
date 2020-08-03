# coding: UTF-8
import requests
import json
import pprint
import os
import datetime
import re
import csv
import urllib3
from requests.auth import HTTPBasicAuth

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


DNAC_URL = '<Cisco DNA Center IP Address>'
DNAC_URI = 'https://<Cisco DNA Center IP Address>'
DNAC_USER = '<username>'
DNAC_PASS = '<password>'



def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://{}/dna/system/api/v1/auth/token'.format(DNAC_URL)                      # Endpoint URL
    hdr = {'content-type' : 'application/json'}                                           # Define request header
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), headers=hdr,verify=False)      # Make the POST Request
    token = resp.json()['Token']                                                          # Retrieve the Token
    #print("Token Retrieved: {}".format(token))                                            # Print out the Token
    return token    # Create a return statement to send the token back for later use


def get_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://{}/api/v1/network-device/15/40".format(DNAC_URL)
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    device_list = resp.json()
    print("{0:25}{1:25}".format("hostname", "id"))
    for device in device_list['response']:
        print("{0:25}{1:25}".format(device['hostname'], device['id']))


def get_deviceconfigbyid(token, url):
    deviceid = input('Please enter device id -> ')

    api_call = '/api/v1/network-device/'
    url += api_call
    url += deviceid
    url += '/config'
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    configdata = json.dumps(response, indent=4).replace('\\n', '\n')
    #print(configdata)

    d = datetime.datetime.now()
    hn = str()

    with open("configbyid.txt", "w") as file:
        file.write(configdata)

    ld = open('configbyid.txt', 'r')
    lines = ld.readlines()
    ld.close()
    for line in lines:
        if line.find("hostname") >= 0:
            hn = str(line[:-1])
            hn2 = hn.replace("hostname ","")

    with open("configbyid.txt", "w") as file:
        file.write(configdata)
        os.rename('configbyid.txt', '{0:%Y%m%d%H%M%S}_{1}.txt'.format(d,hn2))
    print('*'*100)
    print('コンフィグデータをテキストファイルに出力しました')
    print('*'*100)
