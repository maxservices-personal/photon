from dataclasses import dataclass
from types import ModuleType
from photon.helpers.apphelpers.app_settings import AppSettings
from pathlib import Path

@dataclass
class App:
    path: Path = None
    settings: AppSettings = None
    app_label: str = None
    module: ModuleType = None
    module_dir: str = None