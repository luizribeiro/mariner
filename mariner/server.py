import os
import logging

from flask import Flask, render_template
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


@app.route("/data", methods=["GET"])
def hello() -> str:
    try:
        elegoo_mars = ElegooMars()
        elegoo_mars.open()

        response = "Hello, World!\n"
        response += f"Firmware Version: {elegoo_mars.get_firmware_version()}\n"
        response += f"State: {elegoo_mars.get_state()}\n"

        return response.replace("\n", "<br />")
    except Exception as ex:
        return f"Error: {str(ex)}<br />"
    finally:
        try:
            elegoo_mars.close()
        except Exception:
            pass


def main() -> None:
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(app, host="0.0.0.0", port=5000)
