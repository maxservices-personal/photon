# from typing import override



class Middleware:
    def before(self, request, context):
        pass

    def after(self, request, response, context):
        pass
