import io
import os

import png
from flask_caching import Cache

from mariner.config import FILES_DIRECTORY
from mariner.file_formats import SlicedModelFile
from mariner.file_formats.utils import get_file_format
from mariner.server.app import app


cache = Cache(app)


@cache.memoize(timeout=0)
def read_cached_sliced_model_file(filename: str) -> SlicedModelFile:
    assert os.path.isabs(filename)
    file_format = get_file_format(filename)
    return file_format.read(FILES_DIRECTORY / filename)


@cache.memoize(timeout=0)
def read_cached_preview(filename: str) -> bytes:
    assert os.path.isabs(filename)
    bytes = io.BytesIO()
    file_format = get_file_format(filename)
    preview_image: png.Image = file_format.read_preview(FILES_DIRECTORY / filename)
    preview_image.write(bytes)
    return bytes.getvalue()
