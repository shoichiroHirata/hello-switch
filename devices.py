import os
import requests
import base64
import hashlib
import hmac
import time
import uuid
from dotenv import load_dotenv

load_dotenv()
token = os.environ["SWITCHBOT_TOKEN"]

secret = os.environ["SWITCHBOT_SECRET"]

# 電子署名
t = str(int(time.time() * 1000))
nonce = str(uuid.uuid4())
string_to_sign = token + t + nonce

sign = base64.b64encode(
    hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()
).decode()

response = requests.get(
    "https://api.switch-bot.com/v1.1/devices", 
    headers={
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce, 
        },
    )

data = response.json()

print("statusCode: ", data["statusCode"])
for device in data["body"]["infraredRemoteList"]:
    print(device["deviceName"], device["remoteType"])

