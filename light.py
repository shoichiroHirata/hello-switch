import os
import sys
import requests

from switchbot_api import BASE_URL, make_headers

device_id = os.environ["SWITCHBOT_LIGHT_ID"]

if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
    sys.exit("使い方: python light.py on|off")

command = "turnOn" if sys.argv[1] == "on" else "turnOff"

response = requests.post(
    f"{BASE_URL}/devices/{device_id}/commands",
    headers=make_headers(),
    json={
        "command": command,
        "parameter": "default",
        "commandType": "command",
    },
)

data = response.json()

print("statusCode:", data["statusCode"])
print("message:", data["message"])
