import geopy.distance
from geopy import Nominatim

# import requests
#
# url = "http://api.geonames.org/geoCodeAddressJSON?username=ti010&q="
#
#
# def coordinates(query: str):
#     response = requests.get(f"{url}{query}")
#     if response.status_code == 200:
#         data = response.json()
#         return data['address']["lat"], data['address']["lng"]

g = Nominatim(user_agent="MLDisambiguatorPOC")


def coordinates(query: str):
    res = g.geocode(query)
    if res is None:
        return 0, 0
    _, coords = res
    return coords


def distance(p1, p2):
    return geopy.distance.distance(p1, p2).km


def names_to_distance(q1: str, q2: str):
    return distance(coordinates(q1), coordinates(q2))


if __name__ == "__main__":
    c1 = coordinates("Salamanca, ES")
    c2 = coordinates("Warsaw, PL")
    print(c1)
    print(c2)
    print(distance(c1, c2))
