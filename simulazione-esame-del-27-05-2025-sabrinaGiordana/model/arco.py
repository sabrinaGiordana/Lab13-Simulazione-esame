from dataclasses import dataclass

from model.drivers import Drivers


@dataclass
class Arco:
    p1: Drivers
    p2: Drivers
    weight: int

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __hash__(self):
        return hash((self.p1, self.p2))
