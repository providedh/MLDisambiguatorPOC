import geopy.distance
import requests

url = "http://api.geonames.org/geoCodeAddressJSON?username=ti010&q="


def coordinates(query: str):
    response = requests.get(f"{url}{query}")
    if response.status_code == 200:
        data = response.json()
        return data["lat"], data["lng"]


def distance(p1, p2):
    return geopy.distance.distance(p1, p2).km
