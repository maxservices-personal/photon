import os
import mimetypes
from photon.core.response.response import Response

def file_iterator(file_path, chunk_size=8192):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


class FileResponse(Response):

    def __init__(self, file_path, download=False):
        super().__init__()
        self.file_path = file_path
        self.download = download

    def _complete_response(self, start_response):
        self.handle_error_codes()
        if not os.path.exists(self.file_path):
            start_response(
                "404 Not Found",
                [("Content-Type", "text/plain")]
            )
            return [b"File not found"]

        file_size = os.path.getsize(self.file_path)
        content_type, _ = mimetypes.guess_type(self.file_path)
        content_type = content_type or "application/octet-stream"

        headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(file_size)),
        ]

        if self.download:
            filename = os.path.basename(self.file_path)
            headers.append(
                ("Content-Disposition", f'attachment; filename="{filename}"')
            )

        start_response("200 OK", headers)

        return file_iterator(self.file_path)
