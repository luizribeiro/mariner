import io
import os

import png
from flask_caching import Cache

from mariner.config import FILES_DIRECTORY
from mariner.file_formats.ctb import CTBFile
from mariner.file_formats.cbddlp import CBDDLPFile
from mariner.server.app import app


cache = Cache(app)


@cache.memoize(timeout=0)
def read_cached_ctb_file(filename: str) -> CTBFile:
    assert os.path.isabs(filename)
    return CTBFile.read(FILES_DIRECTORY / filename)

@cache.memoize(timeout=0)
def read_cached_cbddlp_file(filename: str) -> CBDDLPFile:
    assert os.path.isabs(filename)
    return CBDDLPFile.read(FILES_DIRECTORY / filename)

@cache.memoize(timeout=0)
def read_cached_preview(filename: str) -> bytes:
    assert os.path.isabs(filename)
    bytes = io.BytesIO()
    preview_image: png.Image = CBDDLPFile.read_preview(FILES_DIRECTORY / filename)
    preview_image.write(bytes)
    return bytes.getvalue()
