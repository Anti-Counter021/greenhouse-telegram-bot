import json

from requests import Session

from . import SITE


class AbstractRequest:

    url: str = ''

    def __init__(self):
        self.session = Session()
        self.base_url: str = SITE

    def load_json(self) -> str:
        response = self.session.get(self.base_url + self.url)
        response.raise_for_status()
        return json.loads(response.text)
