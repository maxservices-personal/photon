from photon.core.config import settings
from photon.helpers.management.app import App
from pathlib import Path
from photon.core.routing import Route, Router
from photon.core.response import FileResponse, HttpResponse

paths: list[Path] = []

class StaticHandler:

    def __init__(self, installed_apps: list[App]):
        self.installed_apps = installed_apps

        self.app_static_routes = []
        self.app_dirs = self._normalize_app_static_dirs()
        self.app_available_dir = []
        self.all_static_dir: list[Path] = []
        self.is_app_level = settings.STATIC.get("APP_LEVEL", False)

        self._load_static_routes()

    def _normalize_app_static_dirs(self):
        app_dirs = settings.STATIC.get("DIRS", "static")

        if isinstance(app_dirs, str):
            return [app_dirs]

        if isinstance(app_dirs, (list, tuple, set)):
            return list(app_dirs)

        raise TypeError("STATIC['APP_DIRS'] must be str or iterable")
    
    def _load_static_routes(self):
        for dir in self.app_dirs:
            path = Path(dir)
            if (settings.PROJECT_PATH==path.parent.absolute()):
                self.app_available_dir.append(path.relative_to(settings.PROJECT_PATH))

            if path.exists(): self.all_static_dir.append(path)

        if not self.is_app_level: return

        for app in self.installed_apps:
            paths_availble = []

            for path in self.app_available_dir:
                full_path = Path(app.module_dir / path)

                if full_path.exists(): paths_availble.append(full_path)
            
            self.all_static_dir.extend(paths_availble)

        return self.all_static_dir


    def define_routes(self, proj_routes:list):

        global paths 
        paths = self.all_static_dir
        router = Router()
        router[Route.get(path="/static/<path>",handler=static_handler, name="photonstatic_func", middlewares=[]),]
        router.setup()
        proj_routes.extend(router._get_routes())

        return proj_routes

def static_handler(request, ctx, path):
    global paths

    for spt in paths:
        sptfp = Path(spt / path)
        if sptfp.exists():
            return FileResponse(str(sptfp))
    
    return HttpResponse("404 Not Found", status_code=404)