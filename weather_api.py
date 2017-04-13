# key = d0d251a70ea814756896149ac8bcd3b3
# http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}
import requests
import json


def create_url(lat, long):
    return "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(long) + "&appid=d0d251a70ea814756896149ac8bcd3b3"


def kelvin_to_farenheit(temp):
    return temp * 9/5 - 459.67


def get_temp(lat, long):
    url = create_url(lat, long)
    json_data = requests.get(url).content
    data = json.loads(json_data)
    temp = data["main"]["temp"]
    return int(kelvin_to_farenheit(int(temp)))


