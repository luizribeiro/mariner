from pathlib import Path
from typing import Sequence


def get_frontend_assets_path() -> str:
    potential_paths: Sequence[Path] = [
        Path("./frontend/dist/"),
        Path("/opt/venvs/mariner3d/assets/"),
    ]
    path = next(path for path in potential_paths if path.exists() and path.is_dir())
    return str(path.absolute())
