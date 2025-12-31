

class Response:
    is_streaming = False
    
    STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self):
        pass

    def _complete_response(self, start_response):
        pass

    def handle_error_codes(self):
        """
        Auto-generate body for error responses if empty
        """
        if self.status_code >= 400 and not self.response:
            message = self.STATUS_MESSAGES.get(
                self.status_code, "Error"
            )
            self.response = f"{self.status_code} {message}"

        return self
    
    def _has_header(self, name):
        return any(h[0].lower() == name.lower() for h in self.headers)

    def _ensure_header(self, name, value):
        if not self._has_header(name):
            self.headers.append((name, value))