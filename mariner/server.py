import io
import logging
import multiprocessing
import os
from enum import Enum

import png
from flask import Flask, Response, jsonify, make_response, render_template, request
from flask_caching import Cache
from pyre_extensions import none_throws
from waitress import serve
from whitenoise import WhiteNoise

from mariner.config import FILES_DIRECTORY
from mariner.file_formats.ctb import CTBFile
from mariner.mars import ElegooMars, PrinterState


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

app.config.from_mapping(
    {
        "DEBUG": True,
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "/tmp/mariner/",
        "CACHE_DEFAULT_TIMEOUT": 300,
    }
)
cache = Cache(app)


@cache.memoize(timeout=0)
def _read_ctb_file(filename: str) -> CTBFile:
    return CTBFile.read(FILES_DIRECTORY / filename)


@cache.memoize(timeout=0)
def _read_preview(filename: str) -> bytes:
    bytes = io.BytesIO()
    preview_image: png.Image = CTBFile.read_preview(FILES_DIRECTORY / filename)
    preview_image.write(bytes)
    return bytes.getvalue()


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/api/print_status", methods=["GET"])
def print_status() -> str:
    with ElegooMars() as elegoo_mars:
        selected_file = elegoo_mars.get_selected_file()
        print_status = elegoo_mars.get_print_status()

        if print_status.state == PrinterState.IDLE:
            progress = 0.0
            print_details = {}
        else:
            ctb_file = _read_ctb_file(selected_file)

            if print_status.current_byte == 0:
                current_layer = 1
            else:
                current_layer = (
                    ctb_file.end_byte_offset_by_layer.index(print_status.current_byte)
                    + 1
                )

            progress = (
                100.0
                * none_throws(current_layer - 1)
                / none_throws(ctb_file.layer_count)
            )

            print_details = {
                "current_layer": current_layer,
                "layer_count": ctb_file.layer_count,
                "print_time_secs": ctb_file.print_time_secs,
                "time_left_secs": round(
                    ctb_file.print_time_secs * (100.0 - progress) / 100.0
                ),
            }

        return jsonify(
            {
                "state": print_status.state.value,
                "selected_file": selected_file,
                "progress": progress,
                **print_details,
            }
        )


@app.route("/api/list_files", methods=["GET"])
def list_files() -> str:
    filename_list = os.listdir(FILES_DIRECTORY)
    files = []
    for filename in filename_list:
        ctb_file = _read_ctb_file(filename)
        files.append(
            {
                "filename": filename,
                "print_time_secs": ctb_file.print_time_secs,
            }
        )
    return jsonify(
        {
            "files": files,
        }
    )


@app.route("/api/file_details", methods=["GET"])
def file_details() -> str:
    filename = str(request.args.get("filename"))
    ctb_file = _read_ctb_file(filename)
    return jsonify(
        {
            "filename": ctb_file.filename,
            "bed_size_mm": list(ctb_file.bed_size_mm),
            "height_mm": round(ctb_file.height_mm, 4),
            "layer_count": ctb_file.layer_count,
            "layer_height_mm": round(ctb_file.layer_height_mm, 4),
            "resolution": list(ctb_file.resolution),
            "print_time_secs": ctb_file.print_time_secs,
        }
    )


@app.route("/api/file_preview", methods=["GET"])
def file_preview() -> Response:
    filename = str(request.args.get("filename"))

    preview_bytes = _read_preview(filename)

    response = make_response(preview_bytes)
    response.headers.set("Content-Type", "image/png")
    response.headers.set(
        "Content-Disposition", "attachment", filename=f"{filename}.png"
    )

    return response


class PrinterCommand(Enum):
    START_PRINT = "start_print"
    PAUSE_PRINT = "pause_print"
    RESUME_PRINT = "resume_print"
    CANCEL_PRINT = "cancel_print"
    REBOOT = "reboot"


class CacheBootstrapper(multiprocessing.Process):
    def run(self) -> None:
        os.nice(5)
        filename_list = os.listdir(FILES_DIRECTORY)
        for filename in filename_list:
            _read_ctb_file(filename)
        for filename in filename_list:
            _read_preview(filename)


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
    CacheBootstrapper().start()

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(app, host="0.0.0.0", port=5000)
