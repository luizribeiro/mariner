from functools import lru_cache
from pathlib import Path
from typing import MutableMapping, Optional, Sequence

import toml


def __get_config_filename() -> Optional[str]:
    potential_paths: Sequence[Path] = [
        Path("config.toml"),
        Path("~/.mariner/config.toml"),
        Path("/etc/mariner/config.toml"),
    ]
    try:
        path = next(
            path for path in potential_paths if path.exists() and not path.is_dir()
        )
    except StopIteration:
        return None
    return str(path.absolute())


@lru_cache
def _get_config() -> MutableMapping[str, object]:
    filename = __get_config_filename()
    if filename is None:
        return {}
    with open(filename, "r") as file:
        toml_string = file.read()
        return toml.loads(toml_string)


def get_files_directory() -> Path:
    config = _get_config()
    return Path(str(config.get("files_directory", "/mnt/usb_share")))
