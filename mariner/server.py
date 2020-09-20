import os
import logging
from enum import Enum

from flask import Flask, jsonify, render_template, request
from pyre_extensions import none_throws
from waitress import serve
from whitenoise import WhiteNoise

from mariner.mars import ElegooMars, PrinterState
from mariner.config import FILES_DIRECTORY


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

        if print_status.state == PrinterState.PRINTING:
            progress = (
                100.0
                * none_throws(print_status.current_byte)
                / none_throws(print_status.total_bytes)
            )
        else:
            progress = 0.0

        return jsonify(
            {
                "state": print_status.state.value,
                "selected_file": selected_file,
                "progress": progress,
            }
        )


@app.route("/api/list_files", methods=["GET"])
def list_files() -> str:
    files = os.listdir(FILES_DIRECTORY)
    return jsonify(
        {
            "files": [{"filename": filename} for filename in files],
        }
    )


class PrinterCommand(Enum):
    START_PRINT = "start_print"
    PAUSE_PRINT = "pause_print"
    RESUME_PRINT = "resume_print"
    CANCEL_PRINT = "cancel_print"
    REBOOT = "reboot"


@app.route("/api/printer/command/<command>", methods=["POST"])
def printer_command(command: str) -> str:
    printer_command = PrinterCommand(command)
    with ElegooMars() as elegoo_mars:
        if printer_command == PrinterCommand.START_PRINT:
            # TODO: validate filename before sending it to the printer
            filename = str(request.args.get("filename"))
            elegoo_mars.start_printing(filename)
        elif printer_command == PrinterCommand.PAUSE_PRINT:
            elegoo_mars.pause_printing()
        elif printer_command == PrinterCommand.RESUME_PRINT:
            elegoo_mars.resume_printing()
        elif printer_command == PrinterCommand.CANCEL_PRINT:
            elegoo_mars.stop_printing()
        elif printer_command == PrinterCommand.REBOOT:
            elegoo_mars.reboot()
        return jsonify({"success": True})


def main() -> None:
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(app, host="0.0.0.0", port=5000)
