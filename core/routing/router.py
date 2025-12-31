from photon.core.routing.route import Route

from ..middlewares import Middleware
from typing import Any

class Router:
    def __init__(self, prefix: str = ""):
        self.prefix = self._normalize_prefix(prefix)
        self.routes: list[Route] = []
        self.middlewares: list[Any, Middleware] = []
        self._pending: list[Route] = []

    def use(self, middleware):
        self.middlewares.append(middleware)
        return self


    def __getitem__(self, routes):
        if not isinstance(routes, (list, tuple)):
            raise TypeError("Router expects a list or tuple of Route objects")

        for route in routes:
            if not isinstance(route, Route):
                raise TypeError("Only Route instances can be registered")

        self._pending.extend(routes)
        return self


    def setup(self):
        """
        Finalize pending routes:
        - apply prefix
        - attach router
        - keep route immutability
        """
        for route in self._pending:
            full_path = self._join(self.prefix, route.raw_path)

            finalized = Route(
                method=route.method,
                path=full_path,
                handler=route.handler,
                middlewares=route.middlewares,
                router=self,
                name=route.name
            )

            self.routes.append(finalized)

        self._pending.clear()
        return self


    def include(self, router: "Router"):
        """
        Include routes from another router (must be setup already)
        """
        for route in router._get_routes():
            full_path = self._join(self.prefix, route.raw_path)

            self.routes.append(
                Route(
                    method=route.method,
                    path=full_path,
                    handler=route.handler,
                    middlewares=route.middlewares,
                    router=route.router,
                    name=route.name
                )
            )

        return self


    def _get_routes(self):
        return self.routes

    @staticmethod
    def _normalize_prefix(prefix: str) -> str:
        if not prefix or prefix == "/":
            return ""
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        return prefix.rstrip("/")

    @staticmethod
    def _join(prefix: str, path: str) -> str:
        if not prefix:
            return path or "/"
        if not path or path == "/":
            return prefix
        return f"{prefix}{path}"
