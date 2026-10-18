import os

from switchbot_api import send_command
from weather import get_min_temperature

THRESHOLD = 10

device_id = os.environ["SWITCHBOT_AIRCON_ID"]
min_temperature = get_min_temperature()

print("長崎市の今日の最低気温:", min_temperature, "°C")

if min_temperature <= THRESHOLD:
    data = send_command(device_id, "turnOn")
    print("エアコンをONにしました:", data["message"])
else:
    print(f"{THRESHOLD}°Cより高いので、エアコンはONにしません")