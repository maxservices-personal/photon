from ..core.config import settings

PROJECT_TEMPLATE = {
    "main.py": """from photon import PhotonProject
from router import router

project = PhotonProject()
project.listen(router.setup())
""",

    "router.py": """from photon import Router

router = Router()
""",

    "photon_config.py": f"""# Photon config
{settings._default_settings()}
""",
# TODO: change thisss

    "apps/__init__.py": "",
}
