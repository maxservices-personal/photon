import re
from typing import Dict, Pattern, Callable
from photon.helpers.shortcuts import Undefined, Method

class Route:
    _PARAM_REGEX = re.compile(r"<(?:(int):)?(\w+)>")

    def __init__(
        self,
        method: Method,
        path: str,
        handler: Callable,
        middlewares=None,
        name=None,
        router=None
    ):
        self.method = method.upper()
        self.raw_path = self._normalize_path(path)
        self.handler = handler
        self.middlewares = list(middlewares) if middlewares else []
        self.router = router
        self.name = name if name else Undefined.value

        self.param_names: list[str] = []
        self.param_types: Dict[str, Callable] = {}
        self.pattern: Pattern = self._compile_path(self.raw_path)


    @classmethod
    def get(cls, path: str, handler: Callable, name=None, middlewares=None):
        return cls(Method.GET, path, handler, middlewares, name)

    @classmethod
    def post(cls, path: str, handler: Callable, middlewares=None, name=None):
        return cls(Method.POST, path, handler, middlewares, name)

    @classmethod
    def put(cls, path: str, handler: Callable, middlewares=None, name=None):
        return cls(Method.PUT, path, handler, middlewares, name)

    @classmethod
    def delete(cls, path: str, handler: Callable, middlewares=None, name=None):
        return cls(Method.DELETE, path, handler, middlewares, name)
    
    @classmethod
    def options(cls, path: str, handler: Callable, middlewares=None, name=None):
        return cls(Method.OPTIONS, path, handler, middlewares, name)

    def use(self, middleware):
        """Immutable middleware chaining"""
        return Route(
            method=self.method,
            path=self.raw_path,
            handler=self.handler,
            middlewares=self.middlewares + [middleware],
            router=self.router,
            name=self.name
        )

    def match(self, request_path: str):
        """
        Returns dict of params if matched, else None
        """
        match = self.pattern.fullmatch(request_path or "")
        if not match:
            return None

        params = match.groupdict()

        for name, caster in self.param_types.items():
            params[name] = caster(params[name])

        return params

    def _compile_path(self, path: str) -> Pattern:
        """
        /api/data/<int:id> → ^/api/data/(?P<id>\d+)$
        """
        regex = "^"
        last_index = 0

        for match in self._PARAM_REGEX.finditer(path):
            start, end = match.span()
            type_name, param_name = match.groups()

            regex += re.escape(path[last_index:start])

            if type_name == "int":
                regex += rf"(?P<{param_name}>\d+)"
                self.param_types[param_name] = int
            else:
                regex += rf"(?P<{param_name}>[^/]+)"
                self.param_types[param_name] = str

            self.param_names.append(param_name)
            last_index = end

        regex += re.escape(path[last_index:])
        regex += "$"

        return re.compile(regex)

    @staticmethod
    def _normalize_path(path: str) -> str:
        return path.rstrip("/") or "/"
