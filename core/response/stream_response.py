from typing import Callable, Generator, Iterable
import json
from . import Response


class StreamResponse(Response):
    is_streaming = True
    def __init__(
        self,
        iterator: Callable[[], Iterable],
        status_code: int = 200,
        headers=None,
        json_response: bool = False,
    ):
        super().__init__()
        self.iterator = iterator
        self.status_code = status_code
        self.headers = headers or []
        self.json_response = json_response

    def _complete_response(self, start_response):
        self.handle_error_codes()

        status_text = self.STATUS_MESSAGES.get(self.status_code, "Unknown Status")
        status_line = f"{self.status_code} {status_text}"

        headers = list(self.headers)

        if self.json_response:
            self._ensure_header(
                "Content-Type", "application/json; charset=utf-8"
            )
        else:
            self._ensure_header(
                "Content-Type", "text/plain; charset=utf-8"
            )

        headers.extend(self.headers)

        start_response(status_line, headers)

        for chunk in self.iterator():
            if chunk is None:
                continue

            if self.json_response:
                chunk = json.dumps(chunk, ensure_ascii=False)

            if isinstance(chunk, str):
                chunk = chunk.encode("utf-8")

            yield chunk