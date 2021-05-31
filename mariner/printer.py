import os
import re
from dataclasses import dataclass
from enum import Enum
from types import TracebackType
from typing import Match, Optional, Type

import serial

from mariner import config
from mariner.exceptions import UnexpectedPrinterResponse


class PrinterState(Enum):
    IDLE = "IDLE"
    STARTING_PRINT = "STARTING_PRINT"
    PRINTING = "PRINTING"
    PAUSED = "PAUSED"


@dataclass(frozen=True)
class PrintStatus:
    state: PrinterState
    current_byte: Optional[int] = None
    total_bytes: Optional[int] = None


class ChiTuPrinter:
    _serial_port: serial.Serial

    def __init__(self) -> None:
        self._serial_port = serial.Serial(
            baudrate=config.get_printer_baudrate(),
            timeout=0.1,
        )

    def _extract_response_with_regex(self, regex: str, data: str) -> Match[str]:
        match = re.search(regex, data)
        if match is None:
            raise UnexpectedPrinterResponse(data)
        return match

    def open(self) -> None:
        self._serial_port.port = config.get_printer_serial_port()
        self._serial_port.open()

    def close(self) -> None:
        self._serial_port.close()

    def __enter__(self) -> "ChiTuPrinter":
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        self.close()
        return False

    def get_firmware_version(self) -> str:
        data = self._send_and_read(b"M4002")
        return self._extract_response_with_regex("^ok ([a-zA-Z0-9_.]+)\n$", data).group(
            1
        )

    def get_state(self) -> str:
        return self._send_and_read(b"M4000")

    def get_print_status(self) -> PrintStatus:
        data = self._send_and_read(b"M4000")
        match = self._extract_response_with_regex("D:([0-9]+)/([0-9]+)/([0-9]+)", data)

        current_byte = int(match.group(1))
        total_bytes = int(match.group(2))
        is_paused = match.group(3) == "1"

        if total_bytes == 0:
            return PrintStatus(state=PrinterState.IDLE)

        if current_byte == 0:
            state = PrinterState.STARTING_PRINT
        elif is_paused:
            state = PrinterState.PAUSED
        else:
            state = PrinterState.PRINTING

        return PrintStatus(
            state=state,
            current_byte=current_byte,
            total_bytes=total_bytes,
        )

    def get_z_pos(self) -> float:
        data = self._send_and_read(b"M114")
        return float(self._extract_response_with_regex("Z:([0-9.]+)", data).group(1))

    def get_selected_file(self) -> str:
        data = self._send_and_read(b"M4006")
        selected_file = str(
            self._extract_response_with_regex("ok '([^']+)'\r\n", data).group(1)
        )
        # normalize the selected file by removing the leading slash, which is
        # sometimes returned by the printer
        return re.sub("^/", "", selected_file)

    def select_file(self, filename: str) -> None:
        response = self._send_and_read((f"M23 /{filename}").encode())
        if "File opened" not in response:
            raise UnexpectedPrinterResponse(response)

    def move_by(self, z_dist_mm: float, mm_per_min: int = 600) -> None:
        response = self._send_and_read(
            (f"G0 Z{z_dist_mm:.1f} F{mm_per_min} I0").encode()
        )
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def move_to(self, z_pos: float) -> str:
        return self._send_and_read((f"G0 Z{z_pos:.1f}").encode())

    def move_to_home(self) -> None:
        response = self._send_and_read(b"G28")
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def start_printing(self, filename: str) -> None:
        # the printer's firmware is weird when the file is in a subdirectory. we need to
        # send M23 to select the file with its full path and then M6030 with just the
        # basename.
        self.select_file(filename)
        response = self._send_and_read(
            (f"M6030 '{os.path.basename(filename)}'").encode(),
            # the mainboard takes longer to reply to this command, so we override the
            # timeout to 2 seconds
            timeout_secs=2.0,
        )
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def pause_printing(self) -> None:
        response = self._send_and_read(b"M25")
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def resume_printing(self) -> None:
        response = self._send_and_read(b"M24")
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def stop_printing(self) -> None:
        response = self._send_and_read(b"M33")
        if "Error" in response:
            raise UnexpectedPrinterResponse(response)

    def stop_motors(self) -> None:
        response = self._send_and_read(b"M112")
        if "ok" not in response:
            raise UnexpectedPrinterResponse(response)

    def reboot(self, delay_in_ms: int = 0) -> None:
        self._send((f"M6040 I{delay_in_ms}").encode())

    def _send_and_read(self, data: bytes, timeout_secs: Optional[float] = None) -> str:
        self._serial_port.reset_input_buffer()
        self._serial_port.reset_output_buffer()

        self._send(data + b"\r\n")

        original_timeout = self._serial_port.timeout
        if timeout_secs is not None:
            self._serial_port.timeout = timeout_secs
        response = self._serial_port.readline().decode("utf-8")
        if timeout_secs is not None:
            self._serial_port.timeout = original_timeout
        # TODO actually read the rest of the response instead of just
        # flushing it like this
        self._serial_port.read(size=1024)
        return response

    def _send(self, data: bytes) -> None:
        self._serial_port.write(data)
