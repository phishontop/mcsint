from .punishment import PunishmentFactory
from bs4 import BeautifulSoup, builder_registry

import requests


class Server:

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.105 Safari/537.36"}

    def _get_history_url(self, text: str) -> str:
        text_dict = {
            "Redirecting": 1,
            "document.location": 5
        }

        for check, value in text_dict.items():
            if check in text:
                value = text.split('"')[value]
                return f"{self.url}/bans/{value}"
            
        return ""

    def get_punishments(self, name: str):
        response = self.session.get(f"{self.url}/bans/check.php?name={name}&table=bans")
        history_url = self._get_history_url(response.text)
        if history_url:
            history_response = requests.get(history_url)
            soup = BeautifulSoup(
                history_response.text,
                builder=builder_registry.lookup(*BeautifulSoup.DEFAULT_BUILDER_FEATURES)
            )

            return PunishmentFactory.create(soup=soup)

        else:
            return []
