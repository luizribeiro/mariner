import re
from dataclasses import dataclass
from enum import Enum
from types import TracebackType
from typing import Optional, Type

import serial
from pyre_extensions import none_throws

from mariner.exceptions import UnexpectedResponse


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


class ElegooMars:
    _serial_port: serial.Serial

    def __init__(self) -> None:
        self._serial_port = serial.Serial(
            baudrate=115200,
            timeout=0.1,
        )

    def open(self) -> None:
        self._serial_port.port = "/dev/serial0"
        self._serial_port.open()

    def close(self) -> None:
        self._serial_port.close()

    def __enter__(self) -> "ElegooMars":
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
        return none_throws(
            re.search("^ok ([a-zA-Z0-9_.]+)\n$", data),
            "Received invalid status response from printer",
        ).group(1)

    def get_state(self) -> str:
        return self._send_and_read(b"M4000")

    def get_print_status(self) -> PrintStatus:
        data = self._send_and_read(b"M4000")
        match = none_throws(
            re.search("D:([0-9]+)/([0-9]+)/([0-9]+)", data),
            "Received invalid status response from printer",
        )

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
        return float(
            none_throws(
                re.search("Z:([0-9.]+)", data),
                "Received invalid status response from printer",
            ).group(1)
        )

    def get_selected_file(self) -> str:
        data = self._send_and_read(b"M4006")
        return str(
            none_throws(
                re.search("ok '([^']+)'\r\n", data),
                "Received invalid status response from printer",
            ).group(1)
        )

    def select_file(self, filename: str) -> None:
        response = self._send_and_read((f"M23 {filename}").encode())
        if "File opened" not in response:
            raise UnexpectedResponse(response)

    def move_by(self, z_dist_mm: float, mm_per_min: int = 600) -> None:
        response = self._send_and_read(
            (f"G0 Z{z_dist_mm:.1f} F{mm_per_min} I0").encode()
        )
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def move_to(self, z_pos: float) -> str:
        return self._send_and_read((f"G0 Z{z_pos:.1f}").encode())

    def move_to_home(self) -> None:
        response = self._send_and_read(b"G28")
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def start_printing(self, filename: str) -> None:
        response = self._send_and_read((f"M6030 '{filename}'").encode())
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def pause_printing(self) -> None:
        response = self._send_and_read(b"M25")
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def resume_printing(self) -> None:
        response = self._send_and_read(b"M24")
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def stop_printing(self) -> None:
        response = self._send_and_read(b"M33")
        if "Error" in response:
            raise UnexpectedResponse(response)

    def stop_motors(self) -> None:
        response = self._send_and_read(b"M112")
        if "ok" not in response:
            raise UnexpectedResponse(response)

    def reboot(self, delay_in_ms: int = 0) -> None:
        self._send((f"M6040 I{delay_in_ms}").encode())

    def _send_and_read(self, data: bytes) -> str:
        self._send(data)

        response = self._serial_port.readline().decode("utf-8")
        # TODO actually read the rest of the response instead of just
        # flushing it like this
        self._serial_port.read(size=1024)
        return response

    def _send(self, data: bytes) -> None:
        self._serial_port.write(data)

    # M20: list files

    # M25: pause printing
    # M24: resume printing
    # M33: stop printing

    # M6030: start printing
