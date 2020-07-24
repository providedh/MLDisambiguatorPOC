import csv
from pprint import pprint

import requests


class Persons:
    api_key = "80e5cd00"
    api_link = "https://my.api.mockaroo.com/providedh-entity-person.json"

    def __init__(self, data_source: str = None):
        if data_source is None:
            self.data = None
            self._download_data()
        else:
            with open(data_source, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                self._data = list(reader)

    def _download_data(self):
        header = {"X-API-Key": self.api_key}
        response = requests.get(self.api_link, headers=header)
        self.data = response.json()

    def gen(self):
        while True:
            for person in self.data:
                yield person
            self._download_data()

    def get(self, n: int):
        g = self.gen()
        d = (g.__next__() for _ in range(n))
        return d

    def dump(self, n: int, filename: str = "dataset.csv"):
        data = self.get(n)

        fields = ["id", "title", "first_name", "last_name", "name_suffix", "gender", "city", "country", "birth_date"]

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)


if __name__ == "__main__":
    p = Persons()
    p.dump(100)
