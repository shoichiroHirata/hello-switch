import os
import requests
import base64
import hashlib
import hmac
import time
import uuid
from dotenv import load_dotenv

from switchbot_api import BASE_URL, make_headers

response = requests.get(f"{BASE_URL}/devices", headers=make_headers())
data = response.json()

print("statusCode: ", data["statusCode"])
for device in data["body"]["infraredRemoteList"]:
    print(device["deviceName"], device["remoteType"])

