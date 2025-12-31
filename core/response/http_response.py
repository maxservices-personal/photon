import json
from photon.core.response.response import Response


class HttpResponse(Response):

    def __init__(self, response=b"", status_code=200, headers=None, json_response=False):
        super().__init__()
        self.response = response
        self.headers = headers or []
        self.status_code = status_code
        self.json_response = json_response

    def _complete_response(self, start_response):
        self.handle_error_codes()

        body = self.response

        if self.json_response:
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self._ensure_header("Content-Type", "application/json; charset=utf-8")

        elif isinstance(body, str):
            body = body.encode("utf-8")

        elif body is None:
            body = b""

        status_text = self.STATUS_MESSAGES.get(self.status_code, "Unknown Status")
        status_line = f"{self.status_code} {status_text}"
        headers = list(self.headers)
        headers.append(("Content-Length", str(len(body))))

        if not self._has_header("Content-Type"):
            headers.append(("Content-Type", "text/plain; charset=utf-8"))

        start_response(status_line, headers)
        return [body]