import importlib.util
from ...core.config import settings

def run(argv):
    main_file_path = settings.BASE_DIR / "main.py"

    if not main_file_path.exists():
        raise FileNotFoundError(
            "'main.py' file does not exist in the current project. "
            "Please ensure that you are running a Photon project."
        )

    spec = importlib.util.spec_from_file_location("photon_main", main_file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {main_file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "main") or not callable(module.main):
        raise AttributeError(
            "'main.py' must define a callable main() function"
        )

    module.main()
