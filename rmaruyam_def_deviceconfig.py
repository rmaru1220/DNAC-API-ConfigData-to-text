# coding: UTF-8
import requests
import json
import pprint
import os
import datetime
import re
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DNAC_URL = 'https://<DNAC IP Address>/api'
DNAC_URI = 'https://<DNAC IP Address>'
DNAC_USER = ''
DNAC_PASSWORD = ''

def get_token(url, user, password):
    api_call = '/system/v1/auth/token'
    url += api_call
    response = requests.post(url=url, auth=(user, password), verify=False).json()
    return response["Token"]


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


def get_tasks(token, url):
    api_call = '/v1/task'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    #print(type(response['response']))
    #print(len(response['response']))
    print(json.dumps(response['response']))
