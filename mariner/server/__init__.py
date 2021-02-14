import logging
import multiprocessing
import os

from flask import render_template
from waitress import serve

from mariner.config import FILES_DIRECTORY
from mariner.server.api import api as api_blueprint
from mariner.server.app import app as flask_app
from mariner.server.utils import (
    read_cached_ctb_file,
    read_cached_preview,
)

from itertools import chain


flask_app.register_blueprint(api_blueprint)


@flask_app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


class CacheBootstrapper(multiprocessing.Process):
    def run(self) -> None:
        os.nice(5)
        for file in chain(
            FILES_DIRECTORY.rglob("*.ctb"), FILES_DIRECTORY.rglob("*.cbddlp")
        ):
            read_cached_ctb_file(file.absolute())
        for file in chain(
            FILES_DIRECTORY.rglob("*.ctb"), FILES_DIRECTORY.rglob("*.cbddlp")
        ):
            read_cached_preview(file.absolute())


def main() -> None:
    CacheBootstrapper().start()

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(flask_app, host="0.0.0.0", port=5000)
