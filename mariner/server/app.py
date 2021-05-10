import os
from pathlib import Path
from typing import Sequence

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from whitenoise import WhiteNoise

from mariner import config


def get_frontend_assets_path() -> str:
    potential_paths: Sequence[Path] = [
        Path("./frontend/dist/"),
        Path("/opt/venvs/mariner3d/dist/"),
    ]
    try:
        path = next(path for path in potential_paths if path.exists() and path.is_dir())
    except StopIteration:
        # fallback to potential_paths. we're likely running from tests
        path = potential_paths[0]
    return str(path.absolute())


frontend_dist_directory: str = get_frontend_assets_path()
app: Flask = Flask(
    __name__,
    template_folder=frontend_dist_directory,
    static_folder=frontend_dist_directory,
)
csrf = CSRFProtect(app)
# pyre-ignore[8]: incompatible attribute type
app.wsgi_app = WhiteNoise(app.wsgi_app)
# pyre-ignore[16]: undefined attribute
app.wsgi_app.add_files(frontend_dist_directory)

app.config.from_mapping(
    {
        "DEBUG": True,
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": config.get_cache_directory(),
        "CACHE_DEFAULT_TIMEOUT": 300,
        "SECRET_KEY": os.urandom(16),
    }
)
