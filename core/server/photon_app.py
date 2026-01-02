import os
from wsgiref.simple_server import make_server
from photon.core.request import Request
from photon.core.response import HttpResponse, FileResponse, Response
from photon.core.routing import Route
from photon.helpers.errors import MethodNotAllowedError
from photon.helpers.shortcuts import Method
from photon.core.config import settings

class PhotonProject:
    def __init__(self):
        self.router = None
        self.routes: list[Route] = []
        
        self.middlewares = []
        self.debug = settings.DEBUG
        self.port = settings.PORT
        self.host = settings.HOST
        # self._load_default_middlewares()

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def listen(self, router, host: str | None = None):
        self.router = router
        self.routes = self.router._get_routes()

        host = self._normalize_host(self.host)

        with make_server(host, self.port, self._project_handler) as server:
            self._print_startup_message(server, host)
            server.serve_forever()

    def _normalize_host(self, host: str | None) -> str:
        """
        Normalize host binding for WSGI server
        """
        if not host or host == "0.0.0.0":
            return ""
        if host == "localhost":
            return "127.0.0.1"
        return host


    def _print_startup_message(self, server, host):
        addr, port = server.socket.getsockname()

        display_host = host if host else "localhost"

        mode = settings.ENV

        print(
            f"\n\nPhoton running in {mode.upper()} mode\n"
            f"➜  http://{display_host}:{port}\n"
            f"Press CTRL+C to quit"
        )
        if self.debug:
            print("\n⚠️  Debug mode is ON. Do not use in production environments!")
        print("\n\n")

    def _load_default_middlewares(self):
        for mw in settings.MIDDLEWARE:
            module_path, class_name = mw.rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            middleware_class = getattr(module, class_name)
            middleware_instance = middleware_class()
            self.add_middleware(middleware_instance)
            
    def _execute_middleware(self, middlewares, request, ctx, _typ, response=None):
        executed = ctx.setdefault("_executed_mw", [])

        for mw in middlewares:
            if _typ == "before_request" and hasattr(mw, "before"):
                res = mw.before(request, ctx)
                executed.append(mw)
                if isinstance(res, Response):
                    return res

            elif _typ == "after_response" and hasattr(mw, "after"):
                if mw in executed:
                    mw.after(request, response, ctx)

        return response

    def _resolve_route(self, request):
        allowed_methods = set()

        for route in self.routes:
            params = route.match(request.route)
            if params is None:
                continue

            if route.method != request.method and route.method != Method.OPTIONS:
                allowed_methods.add(route.method)
                continue

            request.params = params
            return route

        if allowed_methods:
            raise MethodNotAllowedError(
                f"Method {request.method} not allowed. Allowed: {', '.join(allowed_methods)}"
            )

        return None

    def _send_static_responses(self, request_path:str):
        if not request_path.startswith(settings.STATIC.get("URL", "/static")): return None
        
        static_folder: list = settings.STATIC.get("DIRS", [])[0]
        _path = request_path.removeprefix(settings.STATIC.get("URL", "/static") + "/")

        full_path = os.path.join(static_folder, _path)

        return FileResponse(full_path)

    def _project_handler(self, environ, start_response):
        request = Request(environ)

        _is_static_serve = self._send_static_responses(request.route)
        if isinstance(_is_static_serve, Response):
            return _is_static_serve._complete_response(start_response)

        context = {}

        try:
            route = self._resolve_route(request)

            if not route:
                response = HttpResponse("404 Not Found", status_code=404)
                return response._complete_response(start_response)
            
            middleware_stack = (
                self.middlewares +
                route.router.middlewares +
                route.middlewares
            )

            for mw in middleware_stack:
                if hasattr(mw, "before"):
                    res = mw.before(request, context)
                    if isinstance(res, Response):
                        return res._complete_response(start_response)
                    
            params = getattr(request, "params", {})
            response = route.handler(request, context, **params)
            if not isinstance(response, Response):
                raise ValueError("Handler must return Response")

            if not getattr(response, "is_streaming", False):
                for mw in reversed(middleware_stack):
                    if hasattr(mw, "after"):
                        mw.after(request, response, context)

            return response._complete_response(start_response)

        except MethodNotAllowedError as e:
            response = HttpResponse(str(e), status_code=405)
            return response._complete_response(start_response)

        except Exception as e:
            response = HttpResponse(str(e), status_code=500)
            return response._complete_response(start_response)
