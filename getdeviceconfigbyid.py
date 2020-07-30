import requests
import json
from rmaruyam_def_deviceconfig import *
from get_device_list import get_device_list

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

auth_token = get_token(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
get_device_list()
get_deviceconfigbyid(auth_token, DNAC_URI)
