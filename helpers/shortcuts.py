from dataclasses import dataclass

@dataclass
class Undefined:
    value = "undefined"

@dataclass
class Method:
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PUT = "PUT"