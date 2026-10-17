import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.environ["SWITCHBOT_TOKEN"]

response = requests.get("https://api.switch-bot.com/v1.0/devices", headers={"Authorization": token})

data = response.json()

print("statusCode: ", data["statusCode"])
for device in data["body"]["infraredRemoteList"]:
    print(device["deviceName"], device["remoteType"])

