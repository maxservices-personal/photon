
from overrides import override
from photon.core.config.loader import ConfigRegistery
from photon.core.response.response import Response
from template_rendering.engine import TemplatingEngine


class TemplateResponse(Response):
    def __init__(self):
        super().__init__()
        self.engine = TemplatingEngine()
        self.config = ConfigRegistery()
        self.static_route = self.config.static_route
        self.template_folder = self.config.template_folder
        self.template_settings = self.config.templating_settings

    @override
    def _complete_response(self, start_response):
        pass

    @override
    def handle_error_codes(self):
        pass