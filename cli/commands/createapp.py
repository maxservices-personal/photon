import os
from ..utils import register_app

APP_TEMPLATE = {
    "router.py": """from photon import Router
from .views import index

router = Router("/{name}")

router[
    # add routes here
]

router.setup()
""",

    "views.py": """from photon import HttpResponse

def index(request, ctx):
    return HttpResponse("Hello from {name}")
""",
}

def run(args):
    if not args:
        print("Usage: photon createapp <app_name>")
        return

    name = args[0]
    path = f"apps/{name}"

    os.makedirs(path, exist_ok=True)

    for file, content in APP_TEMPLATE.items():
        with open(f"{path}/{file}", "w") as f:
            f.write(content.format(name=name))

    register_app(name)
    print(f"App '{name}' created")
