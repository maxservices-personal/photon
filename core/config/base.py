import pathlib
import importlib.util
import json
class Config:
    def __init__(self):
        self.project_root = pathlib.Path.cwd()
        self.config_module = self._load_config_file()
        self.project_config = self.config_module.PROJECT_CONFIG if self.config_module else self.load_default_config("project_config")
        self.middleware_config = self.config_module.MIDDLEWARE_CONFIG if self.config_module else self.load_default_config("middleware_config")
        self.template_config = self.config_module.TEMPLATE_CONFIG if self.config_module else self.load_default_config("template_config")
        

    def load_default_config(self, config_name):
        if config_name == "project_config":
            return {
                "debug": True,
                "port": 2117,
                "state": "development"
            }
        elif config_name == "middleware_config":
            return {
                "default_cors": False,
                "MIDDLEWARES": [
                    "photon.core.middlewares.auth.AuthMiddleware",
                    "photon.core.middlewares.cors.CORSMiddleware",
                    "photon.core.middlewares.session.SessionMiddleware",
                ]
            }
        elif config_name == "template_config":
            return {
                "dirs": [str(self.project_root / "templates")],
                "autoescape": True,
                "engine": [
                    'photon.template_rendering.engines.jinja.Jinja2Engine',
                ],
                "static_dirs": [str(self.project_root / "static")],
                "static_route": "/static"
            }

    def _load_config_file(self):
        config_path = self.project_root / "photon_config.py"
        if config_path.exists():
            spec = importlib.util.spec_from_file_location("photon_config", config_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            return config_module
        return None
    
    def setup_project_config(self):
        return f"""

# Auto-generated configuration file for Photon Project

PROJECT_CONFIG = {json.dumps(self.project_config)}

MIDDLEWARE_CONFIG = {json.dumps(self.middleware_config)}

TEMPLATE_CONFIG = {json.dumps(self.template_config)}
"""