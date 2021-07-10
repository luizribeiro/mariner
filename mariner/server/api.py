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

from mariner import config
from mariner.exceptions import MarinerException, UnexpectedPrinterResponse
from mariner.file_formats import SlicedModelFile
from mariner.file_formats.utils import get_file_extension, get_supported_extensions
from mariner.printer import ChiTuPrinter, PrinterState
from mariner.server.utils import (
    read_cached_preview,
    read_cached_sliced_model_file,
    retry,
)


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
    with ChiTuPrinter() as printer:
        # the printer sends periodic "ok" responses over serial. this means that
        # sometimes we get an unexpected response from the printer (an "ok" instead of
        # the print status we expected). due to this, we retry at most 3 times here
        # until we have a successful response. see issue #180
        selected_file = retry(
            printer.get_selected_file,
            UnexpectedPrinterResponse,
            num_retries=3,
        )
        print_status = retry(
            printer.get_print_status,
            UnexpectedPrinterResponse,
            num_retries=3,
        )

        if print_status.state == PrinterState.IDLE:
            progress = 0.0
            print_details = {}
        else:
            sliced_model_file = read_cached_sliced_model_file(
                config.get_files_directory() / selected_file
            )

            if print_status.current_byte == 0:
                current_layer = 1
            else:
                current_layer = (
                    sliced_model_file.end_byte_offset_by_layer.index(
                        print_status.current_byte
                    )
                    + 1
                )

            progress = (
                100.0
                * none_throws(current_layer - 1)
                / none_throws(sliced_model_file.layer_count)
            )

            print_details = {
                "current_layer": current_layer,
                "layer_count": sliced_model_file.layer_count,
                "print_time_secs": sliced_model_file.print_time_secs,
                "time_left_secs": round(
                    sliced_model_file.print_time_secs * (100.0 - progress) / 100.0
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
    path = (config.get_files_directory() / path_parameter).resolve()
    if (
        config.get_files_directory() not in path.parents
        and path != config.get_files_directory()
    ):
        abort(400)
    with os.scandir(path) as dir_entries:
        files = []
        directories = []
        for dir_entry in sorted(
            dir_entries, key=lambda t: t.stat().st_mtime, reverse=True
        ):
            if dir_entry.is_file():
                sliced_model_file: Optional[SlicedModelFile] = None
                if get_file_extension(dir_entry.name) in get_supported_extensions():
                    if dir_entry.name.startswith("._"):
                        if b"Mac OS X" not in open(dir_entry, "rb").read(32):
                            sliced_model_file = read_cached_sliced_model_file(
                                path / dir_entry.name
                            )
                    else:
                        sliced_model_file = read_cached_sliced_model_file(
                            path / dir_entry.name
                        )

                file_data: Dict[str, Any] = {
                    "filename": dir_entry.name,
                    "path": str(
                        (path / dir_entry.name).relative_to(
                            config.get_files_directory()
                        )
                    ),
                }

                if sliced_model_file:
                    file_data = {
                        "print_time_secs": sliced_model_file.print_time_secs,
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
    path = (config.get_files_directory() / filename).resolve()
    if config.get_files_directory() not in path.parents:
        abort(400)
    sliced_model_file = read_cached_sliced_model_file(path)
    return jsonify(
        {
            "filename": sliced_model_file.filename,
            "path": filename,
            "bed_size_mm": list(sliced_model_file.bed_size_mm),
            "height_mm": round(sliced_model_file.height_mm, 4),
            "layer_count": sliced_model_file.layer_count,
            "layer_height_mm": round(sliced_model_file.layer_height_mm, 4),
            "resolution": list(sliced_model_file.resolution),
            "print_time_secs": sliced_model_file.print_time_secs,
        }
    )


@api.route("/upload_file", methods=["POST"])
def upload_file() -> str:
    file = request.files.get("file")
    if file is None or file.filename == "":
        abort(400)
    if get_file_extension(file.filename) not in get_supported_extensions():
        abort(400)
    filename = secure_filename(file.filename)
    file.save(str(config.get_files_directory() / filename))
    os.sync()
    return jsonify({"success": True})


@api.route("/delete_file", methods=["POST"])
def delete_file() -> str:
    filename = str(request.args.get("filename"))
    path = (config.get_files_directory() / filename).resolve()
    if config.get_files_directory() not in path.parents:
        abort(400)
    # we use os.path.isfile instead of Path.is_file here because pyfakefs doesn't
    # seem to properly mock Path.is_file as of pyfakefs 4.4.0
    if not os.path.isfile(path):
        abort(400)
    os.remove(path)
    return jsonify({"success": True})


@api.route("/file_preview", methods=["GET"])
def file_preview() -> Response:
    filename = str(request.args.get("filename"))
    path = (config.get_files_directory() / filename).resolve()
    if config.get_files_directory() not in path.parents:
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
    with ChiTuPrinter() as printer:
        if printer_command == PrinterCommand.START_PRINT:
            # TODO: validate filename before sending it to the printer
            filename = str(request.args.get("filename"))
            printer.start_printing(filename)
        elif printer_command == PrinterCommand.PAUSE_PRINT:
            printer.pause_printing()
        elif printer_command == PrinterCommand.RESUME_PRINT:
            printer.resume_printing()
        elif printer_command == PrinterCommand.CANCEL_PRINT:
            printer.stop_printing()
        elif printer_command == PrinterCommand.REBOOT:
            printer.reboot()
        return jsonify({"success": True})
