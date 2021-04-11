import io
import os
from typing import Mapping, Type

import png
from flask_caching import Cache

from mariner.config import FILES_DIRECTORY
from mariner.file_formats import SlicedModelFile
from mariner.file_formats.ctb import CTBFile
from mariner.file_formats.cbddlp import CBDDLPFile
from mariner.file_formats.fdg import FDGFile
from mariner.server.app import app


cache = Cache(app)


@cache.memoize(timeout=0)
def read_cached_sliced_model_file(filename: str) -> SlicedModelFile:
    assert os.path.isabs(filename)
    file_format = _get_file_format(filename)
    return file_format.read(FILES_DIRECTORY / filename)


@cache.memoize(timeout=0)
def read_cached_preview(filename: str) -> bytes:
    assert os.path.isabs(filename)
    bytes = io.BytesIO()
    file_format = _get_file_format(filename)
    preview_image: png.Image = file_format.read_preview(FILES_DIRECTORY / filename)
    preview_image.write(bytes)
    return bytes.getvalue()


def _get_file_format(filename: str) -> Type[SlicedModelFile]:
    (_, extension) = os.path.splitext(filename)

    # only reason this is in here is because it makes mocking on
    # mariner.tests.test_server simpler
    EXTENSION_TO_FILE_FORMAT: Mapping[str, Type[SlicedModelFile]] = {
        ".ctb": CTBFile,
        ".cbddlp": CBDDLPFile,
        ".fdg": FDGFile,
    }
    file_format = EXTENSION_TO_FILE_FORMAT.get(extension.lower())

    assert file_format is not None
    return file_format
