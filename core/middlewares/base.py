# Example Base Class For Middleware
# TODO: Add more options and features as needed



class Middleware:
    def before(self, request, context):
        pass

    def after(self, request, response, context):
        pass
