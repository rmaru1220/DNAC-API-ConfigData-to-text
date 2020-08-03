import requests
import json
import urllib3
from rmaruyam_def_deviceconfig import *
from requests.auth import HTTPBasicAuth

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auth_token = get_auth_token()
get_device_list()
get_deviceconfigbyid(auth_token, DNAC_URI)
