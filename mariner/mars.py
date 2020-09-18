import re
from dataclasses import dataclass
from typing import Optional

import serial
from pyre_extensions import none_throws


@dataclass(frozen=True)
class PrintStatus:
    is_printing: bool
    current_byte: Optional[int] = None
    total_bytes: Optional[int] = None


class ElegooMars:
    _serial_port: Optional[serial.Serial] = None

    def open(self) -> None:
        self._serial_port = serial.Serial(
            "/dev/serial0",
            baudrate=115200,
            timeout=0.1,
        )
        none_throws(self._serial_port).open()

    def close(self) -> None:
        none_throws(self._serial_port).close()

    def get_firmware_version(self) -> str:
        data = self._send_and_read(b"M4002")
        return none_throws(
            re.search("^ok ([a-zA-Z0-9_.]+)\n$", data),
            "Received invalid status response from printer",
        ).group(1)

    def get_state(self) -> str:
        return self._send_and_read(b"M4000")

    def get_print_status(self) -> PrintStatus:
        data = self._send_and_read(b"M27")
        if "SD printing byte" in data:
            match = none_throws(
                re.search("SD printing byte ([0-9]+)/([0-9]+)", data),
                "Received invalid status response from printer",
            )
            return PrintStatus(
                is_printing=True,
                current_byte=int(match.group(1)),
                total_bytes=int(match.group(2)),
            )
        elif "It's not printing now" in data:
            return PrintStatus(is_printing=False)

        raise NotImplementedError

    def get_z_pos(self) -> float:
        data = self._send_and_read(b"M114")
        return float(
            none_throws(
                re.search("Z:([0-9.]+)", data),
                "Received invalid status response from printer",
            ).group(1)
        )

    def get_last_selected_file(self) -> str:
        data = self._send_and_read(b"M4006")
        return str(
            none_throws(
                re.search("ok '([^']+)'\r\n", data),
                "Received invalid status response from printer",
            ).group(1)
        )

    def move_to(self, z_pos: float) -> str:
        return self._send_and_read((f"G0 Z{z_pos:.1f}").encode())

    def _send_and_read(self, data: bytes) -> str:
        serial_port = none_throws(
            self._serial_port,
            "Tried to communicate with serial port without opening it",
        )
        serial_port.write(data)
        return serial_port.readline().decode("utf-8")

    # M20: list files

    # M25: pause printing
    # M24: resume printing
    # M33: stop printing

    # M6030: start printing
