from .punishment import PunishmentFactory
from .utilities.soup import Soup

from threading import Thread
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
            soup = Soup.create(html=history_response.text)

            return PunishmentFactory.create(soup=soup)

        else:
            return []


class Servers:

    def __init__(self, name: str) -> None:
        self.servers = Servers.get_sites()
        self.punishments = {}
        self.name = name

    @staticmethod
    def get_sites():
        with open("sites.txt") as file:
            sites = file.readlines()
            return [
                Server(site.replace("\n", ""))
                for site in sites
            ]

    def get_punishments(self, server_object: Server):
        new_punishments = []
        punishments = server_object.get_punishments(name=self.name)
        for punishment in punishments:
            new_punishments.append(punishment.as_dict())

        if len(punishments) > 0:
            self.punishments[server_object.url] = new_punishments

    def lookup(self):
        threads = []
        for server in self.servers:
            threads.append(Thread(target=self.get_punishments, args=(server,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return self.punishments
