import os
import sys

from switchbot_api import send_command

device_id = os.environ["SWITCHBOT_LIGHT_ID"]

if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
    sys.exit("使い方: python light.py on|off")

command = "turnOn" if sys.argv[1] == "on" else "turnOff"

data = send_command(device_id, command)

print("statusCode:", data["statusCode"])
print("message:", data["message"])