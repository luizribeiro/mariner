import logging
import multiprocessing
import os

from flask import render_template
from waitress import serve

from mariner.config import FILES_DIRECTORY
from mariner.file_formats.utils import get_supported_extensions
from mariner.server.api import api as api_blueprint
from mariner.server.app import app as flask_app
from mariner.server.utils import (
    read_cached_preview,
    read_cached_sliced_model_file,
)

from itertools import chain


flask_app.register_blueprint(api_blueprint)


@flask_app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


class CacheBootstrapper(multiprocessing.Process):
    def run(self) -> None:
        os.nice(5)
        globs = [
            FILES_DIRECTORY.rglob(f"*{extension}")
            for extension in get_supported_extensions()
        ]
        for file in chain.from_iterable(globs):
            read_cached_sliced_model_file(file.absolute())
        for file in chain.from_iterable(globs):
            read_cached_preview(file.absolute())


def main() -> None:
    CacheBootstrapper().start()

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(flask_app, host="0.0.0.0", port=5000)
