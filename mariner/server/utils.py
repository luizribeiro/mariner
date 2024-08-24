import io
import os
import time
from typing import Callable, Type, TypeVar

import png
from flask_caching import Cache

from mariner import config
from mariner.file_formats import SlicedModelFile
from mariner.file_formats.utils import get_file_format
from mariner.server.app import app


cache = Cache(app)


@cache.memoize(timeout=0)
def read_cached_sliced_model_file(filename: str) -> SlicedModelFile:
    assert os.path.isabs(filename)
    assert os.path.isfile(filename)
    file_format = get_file_format(filename)
    return file_format.read(config.get_files_directory() / filename)


@cache.memoize(timeout=0)
def read_cached_preview(filename: str) -> bytes:
    assert os.path.isabs(filename)
    assert os.path.isfile(filename)
    bytes = io.BytesIO()
    file_format = get_file_format(filename)
    preview_image: png.Image = file_format.read_preview(
        config.get_files_directory() / filename
    )
    preview_image.write(bytes)
    return bytes.getvalue()


TReturn = TypeVar("TReturn")


def retry(
    func: Callable[[], TReturn],
    exception_type: Type[Exception],
    *,
    num_retries: int,
    delay_ms: int = 100,
) -> TReturn:
    attempts_left = num_retries
    while attempts_left > 0:
        try:
            return func()
        except exception_type:
            attempts_left -= 1
            time.sleep(delay_ms / 1000.0)
    return func()
