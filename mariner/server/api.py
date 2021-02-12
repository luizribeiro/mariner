import os
import traceback
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from flask import (
    Blueprint,
    Response,
    abort,
    jsonify,
    make_response,
    request,
)
from pyre_extensions import none_throws
from werkzeug.utils import secure_filename

from mariner.config import FILES_DIRECTORY
from mariner.exceptions import MarinerException
from mariner.file_formats.ctb import CTBFile
from mariner.mars import ElegooMars, PrinterState
from mariner.server.utils import read_cached_cbddlp_file, read_cached_ctb_file, read_cached_preview


api = Blueprint("api", __name__, url_prefix="/api")


@api.errorhandler(MarinerException)
def handle_mariner_exception(exception: MarinerException) -> Tuple[str, int]:
    tb = traceback.TracebackException.from_exception(exception)
    return (
        jsonify(
            {
                "title": exception.get_title(),
                "description": exception.get_description(),
                "traceback": "".join(tb.format()),
            }
        ),
        500,
    )


@api.route("/print_status", methods=["GET"])
def print_status() -> str:
    with ElegooMars() as elegoo_mars:
        selected_file = elegoo_mars.get_selected_file()
        print_status = elegoo_mars.get_print_status()

        if print_status.state == PrinterState.IDLE:
            progress = 0.0
            print_details = {}
        else:
            ctb_file = read_cached_ctb_file(FILES_DIRECTORY / selected_file)

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


@api.route("/list_files", methods=["GET"])
def list_files() -> str:
    path_parameter = str(request.args.get("path", "."))
    path = (FILES_DIRECTORY / path_parameter).resolve()
    if FILES_DIRECTORY not in path.parents and path != FILES_DIRECTORY:
        abort(400)
    with os.scandir(path) as dir_entries:
        files = []
        directories = []
        for dir_entry in dir_entries:
            if dir_entry.is_file():
                ctb_file: Optional[CTBFile] = None
                cbddlp_file: Optional[CBDDLPFile] = None
                if dir_entry.name.endswith(".cbddlp" or ".ctb"):
                    ctb_file = read_cached_ctb_file(path / dir_entry.name)

                file_data: Dict[str, Any] = {
                    "filename": dir_entry.name,
                    "path": str((path / dir_entry.name).relative_to(FILES_DIRECTORY)),
                }

                if ctb_file:
                    file_data = {
                        "print_time_secs": ctb_file.print_time_secs,
                        "can_be_printed": True,
                        **file_data,
                    }
                elif cbddlp_file:
                    file_data = {
                        "print_time_secs": cbddlp_file.print_time_secs,
                        "can_be_printed": True,
                        **file_data,
                    }
                else:
                    file_data = {
                        "can_be_printed": False,
                        **file_data,
                    }

                files.append(file_data)
            else:
                directories.append({"dirname": dir_entry.name})
        return jsonify(
            {
                "directories": directories,
                "files": files,
            }
        )


@api.route("/file_details", methods=["GET"])
def file_details() -> str:
    filename = str(request.args.get("filename"))
    path = (FILES_DIRECTORY / filename).resolve()
    if FILES_DIRECTORY not in path.parents:
        abort(400)
    ctb_file = read_cached_ctb_file(path)
    return jsonify(
        {
            "filename": ctb_file.filename,
            "path": filename,
            "bed_size_mm": list(ctb_file.bed_size_mm),
            "height_mm": round(ctb_file.height_mm, 4),
            "layer_count": ctb_file.layer_count,
            "layer_height_mm": round(ctb_file.layer_height_mm, 4),
            "resolution": list(ctb_file.resolution),
            "print_time_secs": ctb_file.print_time_secs,
        }
    )


@api.route("/upload_file", methods=["POST"])
def upload_file() -> str:
    file = request.files.get("file")
    if file is None or file.filename == "":
        abort(400)
    if os.path.splitext(file.filename)[1] != (".cbddlp" or ".ctb"):
        abort(400)
    filename = secure_filename(file.filename)
    file.save(str(FILES_DIRECTORY / filename))
    return jsonify({"success": True})


@api.route("/delete_file", methods=["POST"])
def delete_file() -> str:
    filename = str(request.args.get("filename"))
    path = (FILES_DIRECTORY / filename).resolve()
    if FILES_DIRECTORY not in path.parents:
        abort(400)
    if not path.is_file():
        abort(400)
    os.remove(path)
    return jsonify({"success": True})


@api.route("/file_preview", methods=["GET"])
def file_preview() -> Response:
    filename = str(request.args.get("filename"))
    path = (FILES_DIRECTORY / filename).resolve()
    if FILES_DIRECTORY not in path.parents:
        abort(400)

    preview_bytes = read_cached_preview(path)

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


@api.route("/printer/command/<command>", methods=["POST"])
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
