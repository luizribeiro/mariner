import logging

from flask import Flask
from waitress import serve

from mariner.mars import ElegooMars


app = Flask(__name__)


@app.route("/")
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
