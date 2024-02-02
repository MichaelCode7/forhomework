import sys
from io import BytesIO
import requests
from PIL import Image
import argparse


# python main.py --address="Москва, ул. Ак. Королева, 12" --spn="10.002,10.002"

parser = argparse.ArgumentParser()
parser.add_argument('--address')
parser.add_argument('--spn')
args = parser.parse_args()
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

spn, address = args.spn, args.address
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": args.address,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print(f'Error #{response.status_code}')

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
print(toponym_coodrinates)
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn,
    "l": "map",
    "pt": ",".join([toponym_longitude, toponym_lattitude])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
print(response.url)
Image.open(BytesIO(response.content)).show()
