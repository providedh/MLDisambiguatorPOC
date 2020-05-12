import requests


class Persons:
    api_key = "80e5cd00"
    api_link = "https://my.api.mockaroo.com/providedh-entity-person.json"

    def __init__(self):
        self.data = None
        self._download_data()

    def _download_data(self):
        header = {"X-API-Key": self.api_key}
        response = requests.get(self.api_link, headers=header)
        self.data = response.json()

    def __next__(self):
        while True:
            for person in self.data:
                yield person
            self._download_data()
