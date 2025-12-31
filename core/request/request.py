import json
import urllib.parse
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.server_protocol = environ["SERVER_PROTOCOL"]
        self.user_agent = environ["HTTP_USER_AGENT"]
        self.cookie = environ["HTTP_COOKIE"]
        self.request_host = environ["HTTP_HOST"]
        self.content_type = environ["CONTENT_TYPE"]
        self.connection = environ["HTTP_CONNECTION"]
        self.environ = environ
        self.headers = self._parse_headers()
        raw = environ.get("PATH_INFO", "")
        self.route = raw.rstrip("/") or "/"

        self._body = None
        self._json = None
        self._form = None
        self._query = None
    
    def _parse_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                header = key[5:].replace("_", "-").title()
                headers[header] = value
        return headers

    def header(self, name, default=None):
        return self.headers.get(name.title(), default)

    @property
    def body(self):
        if self._body is None:
            length = int(self.environ.get("CONTENT_LENGTH", 0) or 0)
            self._body = self.environ["wsgi.input"].read(length)
        return self._body

    @property
    def text(self):
        return self.body.decode("utf-8", errors="replace")

    def json(self):
        if self._json is not None:
            return self._json

        content_type = self.environ.get("CONTENT_TYPE", "")
        if "application/json" not in content_type:
            return None

        try:
            self._json = json.loads(self.text)
            return self._json
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")

    @property
    def form(self):
        if self._form is not None:
            return self._form

        content_type = self.environ.get("CONTENT_TYPE", "")
        if "application/x-www-form-urlencoded" not in content_type:
            return {}

        parsed = urllib.parse.parse_qs(self.text)
        self._form = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        return self._form

    @property
    def parameters(self):
        """
        Parsed query parameters (?a=1&b=2)
        """
        if self._query is not None:
            return self._query

        raw = self.environ.get("QUERY_STRING", "")
        parsed = parse_qs(raw, keep_blank_values=True)

        self._query = {
            key: values[0] if len(values) == 1 else values
            for key, values in parsed.items()
        }

        return self._query

    def get(self, key, default=None):
        """
        Priority:
        1. route params
        2. query params
        3. form data
        """
        if hasattr(self, "params") and key in self.params:
            return self.params[key]

        if key in self.parameters:
            return self.parameters[key]

        if key in self.form:
            return self.form[key]

        return default