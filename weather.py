import requests

NAGASAKI_LATITUDE = 32.75
NAGASAKI_LONGITUDE = 129.88

def get_min_temperature():
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": NAGASAKI_LATITUDE,
            "longitude": NAGASAKI_LONGITUDE,
            "daily": "temperature_2m_min",
            "timezone": "Asia/Tokyo",
            "forecast_days": 1,
        },
    )
    data = response.json()
    return data["daily"]["temperature_2m_min"][0]

if __name__ == "__main__":
    print("長崎市の今日の最低気温:", get_min_temperature(), "°C")