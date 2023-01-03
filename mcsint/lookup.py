import time
from .plancke import PlanckeScraper
from .server import Servers


class Lookup:

    def __init__(self, name: str):
        self.name = name
        self.stats = {}

    def run(self):
        functions = {
            "hypixel": PlanckeScraper(name=self.name).get_info,
            "punishments": Servers(name=self.name).lookup
        }

        for name, func in functions.items():
            self.stats[name] = func()
