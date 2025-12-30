

class Response:

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
        pass