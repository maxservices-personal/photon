from dataclasses import dataclass

@dataclass
class Undefined:
    value = "undefined"


class Name:
    def __init__(self, name):
        self.value = name

@dataclass
class Method:
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PUT = "PUT"