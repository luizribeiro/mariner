import os
import logging

from flask import Flask, jsonify, render_template
from pyre_extensions import none_throws
from waitress import serve
from whitenoise import WhiteNoise

from mariner.mars import ElegooMars


frontend_dist_directory: str = os.path.abspath("./frontend/dist/")
app = Flask(
    __name__,
    template_folder=frontend_dist_directory,
    static_folder=frontend_dist_directory,
)
# pyre-ignore[8]: incompatible attribute type
app.wsgi_app = WhiteNoise(app.wsgi_app)
# pyre-ignore[16]: undefined attribute
app.wsgi_app.add_files(frontend_dist_directory)


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/api/print_status", methods=["GET"])
def print_status() -> str:
    with ElegooMars() as elegoo_mars:
        selected_file = elegoo_mars.get_selected_file()
        print_status = elegoo_mars.get_print_status()

        if print_status.is_printing:
            progress = (
                100.0
                * none_throws(print_status.current_byte)
                / none_throws(print_status.total_bytes)
            )
        else:
            progress = 0.0

        return jsonify(
            {
                "selected_file": selected_file,
                "is_printing": print_status.is_printing,
                "progress": progress,
            }
        )


def main() -> None:
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(app, host="0.0.0.0", port=5000)
