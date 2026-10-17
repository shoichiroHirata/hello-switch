import base64
import hashlib
import hmac
import os
import time
import uuid

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.switch-bot.com/v1.1"

def make_headers():
    token = os.environ["SWITCHBOT_TOKEN"]

    secret = os.environ["SWITCHBOT_SECRET"]

    # 電子署名
    t = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    string_to_sign = token + t + nonce

    sign = base64.b64encode(
        hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    ).decode()

    return {
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce,    
    }