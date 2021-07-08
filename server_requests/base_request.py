import json

from typing import Dict

from requests import Session

from . import SITE


class AbstractRequest:

    url: str = ''
    headers: Dict[str, str] = {
        'Content-type': 'application/json',
    }

    def __init__(self):
        self.session = Session()
        self.session.headers = self.headers
        self.base_url: str = SITE

    def load_json(self) -> str:
        response = self.session.get(self.base_url + self.url)
        response.raise_for_status()
        return json.loads(response.text)

    def post_json(self, data) -> str:
        response = self.session.post(self.base_url + self.url, json.dumps(data))
        response.raise_for_status()
        return json.loads(response.text)
