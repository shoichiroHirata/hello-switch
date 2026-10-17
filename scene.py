import os
import requests

from switchbot_api import BASE_URL, make_headers

scene_id = os.environ["SWITCHBOT_SCENE_ID"]

# print(scene_id)

response = requests.post(
    f"{BASE_URL}/scenes/{scene_id}/execute",
    headers=make_headers(),
)

data = response.json()

print("statusCode: ", data["statusCode"])
print("message: ", data["message"])