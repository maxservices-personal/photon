from ..engine import TemplateBaseEngine
from jinja2 import (
    Environment,
    FileSystemLoader,
    ChoiceLoader,
    select_autoescape
)

from photon.core.config import settings
from photon.helpers.management.app import App


class Jinja2Engine(TemplateBaseEngine):
    def __init__(self, installed_apps: list[App], **kwargs):
        self.installed_apps = installed_apps
        self._build_environment()

    def _build_environment(self):

        loaders = []

        for directory in settings.TEMPLATES.get("DIRS", []):
            loaders.append(FileSystemLoader(directory))

        if settings.TEMPLATES.get("APP_DIRS", True):
            for app in self.installed_apps:
                loaders.append(
                    FileSystemLoader(f"apps/{app.app_label}/templates")
                )

        autoescape = settings.TEMPLATES.get("AUTOESCAPE", True)

        options = settings.TEMPLATES.get("OPTIONS", {})

        self.env = Environment(
            loader=ChoiceLoader(loaders),
            autoescape=select_autoescape(["html", "xml"]) if autoescape else False,
            **options
        )

    def render_template(self, template_name: str, context: dict | None = None) -> str:
        template = self.env.get_template(template_name)
        return template.render(context or {})
    