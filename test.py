from photon.core.server.photon_app import Photon
from photon.core.routing.router import Router
from photon.core.response.http_response import HttpResponse
from photon.core.request.request import Request
import time

class TimingMiddleware:
    def before_request(self, request, context):
        context["start_time"] = time.time()

    def after_response(self, request, response, context):
        duration = time.time() - context["start_time"]
        print(f"Request {context.get('request_id')} took {duration:.4f}s")


app = Photon()
router = Router()


def hello_world(request: Request, middleware_context: dict):
    return HttpResponse(response="<h1>Hello World!</h1>", headers=[("Content-Type", "text/html")], status_code=200)

router.get("", hello_world)

api_router = Router(prefix="/api/")
api_router.get("", hello_world)
api_router.get("/hello", hello_world)


router.include(api_router)

for respo in router._get_routes():
    print(respo.path)

app.listen(router=router, port=8080)
