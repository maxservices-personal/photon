# Basic Single file implementation of Photon Project with Routing and Middleware

from photon import PhotonProject, HttpResponse, Request, Router, Route
from photon.core.middlewares.setup_middleware import Middleware
from photon.core.config.base import Config
import time
from overrides import override

class TimingMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    @override
    def before(self, request, context):
        context["start_time"] = time.time()

    @override
    def after(self, request, response, context):
        duration = time.time() - context["start_time"]
        print(f"Request {request.route} took {duration:.10f}s")


config = Config()

project = PhotonProject(config)

def home_handler(request: Request, context):
    return HttpResponse({"message": "Welcome to the Photon Project!"}, json_response=True)

def api_handler(request: Request, context, id):
    return HttpResponse({"data": f"This is the API endpoint for ID {id}."}, json_response=True)


main_router = Router()
main_router.use(TimingMiddleware())
main_router[
    Route.get("", home_handler, name="home"),
    Route.get("/hellpo", lambda req, ctx: HttpResponse("Hello World!")),
].setup()


api_router = Router(prefix="/api")
api_router[
    Route.get("/data/<id>/user", api_handler, name="data_handler"),
].setup()

main_router.include(api_router)

project.listen(main_router, 'localhost')