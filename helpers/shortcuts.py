from dataclasses import dataclass

@dataclass
class Undefined:
    value = "undefined"


class Name:
    def __init__(self, name):
        self.value = name