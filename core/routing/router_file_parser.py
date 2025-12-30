import importlib.util

class RouterFileParser:
    def __init__(self, config):
        self.config = config
        self.project_root = self.config.project_root
        self.router_file_path = self.project_root / "routes.py"

    def load_router_file(self):
        if self.router_file_path.exists():
            spec = importlib.util.spec_from_file_location("routes", self.router_file_path)
            routes_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(routes_module)
            return routes_module.router if hasattr(routes_module, "router") else None
        return None