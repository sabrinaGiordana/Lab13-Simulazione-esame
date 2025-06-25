from dataclasses import dataclass

@dataclass
class Drivers:
    driverId: int
    driverRef: str
    number: int
    code: str
    forename: str
    surname: str
    dob: str
    nationality: str
    url: str

    def __str__(self):
        return self.surname + " " + self.forename

    def __hash__(self):
        return hash(self.driverId)
    def __eq__(self, other):
        pass
