import pathlib
import importlib.util
import os
from uuid import uuid4

class Settings:
    """
    Django-style lazy settings object for Photon.
    Loads settings once and exposes them as attributes.
    """

    def __init__(self):
        self._loaded = False
        self._settings = {}
        self.BASE_DIR = pathlib.Path.cwd()

    def load(self):
        if self._loaded:
            return

        self._settings.update(self._default_settings())

        self._load_user_settings()

        self._normalize()
        self._validate()

        self._loaded = True

    def __getattr__(self, name):
        self.load()
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f"Photon setting '{name}' not found")

    def __repr__(self):
        return "<Photon Settings (configured)>"

    def _default_settings(self):
        return {
            "DEBUG": True,
            "ENV": "development",
            "HOST": "127.0.0.1",
            "PORT": 2117,

            "SECRET_KEY": f"photon-default-key-{uuid4()}",

            "INSTALLED_APPS": [],

            "MIDDLEWARE": [],

            "TEMPLATES": {
                "ENGINE": None,
                "DIRS": [],
                "APP_DIRS": True,
                "AUTOESCAPE": True,
                "OPTIONS": {},
            },

            "STATIC": {
                "URL": "/static/",
                "DIRS": [],
                "APP_DIRS": True,
            },

            "DATABASES": {},

            "LOGGING": {
                "LEVEL": "INFO",
                "FORMAT": "simple",
                "ACCESS_LOG": True,
            },
        }

    def _load_user_settings(self):
        config_path = self.BASE_DIR / "photon_config.py"

        if not config_path.exists():
            return

        spec = importlib.util.spec_from_file_location(
            "photon_config", config_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for key in dir(module):
            if key.isupper():
                self._settings[key] = getattr(module, key)

    def _normalize(self):
        tmpl = self._settings["TEMPLATES"]
        tmpl["DIRS"] = [
            str(self.BASE_DIR / d) for d in tmpl.get("DIRS", [])
        ]

        static = self._settings["STATIC"]
        static["DIRS"] = [
            str(self.BASE_DIR / d) for d in static.get("DIRS", [])
        ]

    def _validate(self):
        if not self._settings["SECRET_KEY"] and self._settings["ENV"] == "production":
            raise RuntimeError(
                "SECRET_KEY must be set in production environment"
            )
