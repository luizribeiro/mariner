import re
from typing import Optional

import serial
from pyre_extensions import none_throws


class ElegooMars:
    _serial_port: Optional[serial.Serial] = None

    def open(self) -> None:
        self._serial_port = serial.Serial(
            "/dev/serial0",
            baudrate=115200,
            timeout=0.1,
        )

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

    def move_to(self, z_pos: float) -> str:
        return self._send_and_read((f"G0 Z{z_pos:.1f}").encode())

    def _send_and_read(self, data: bytes) -> str:
        serial_port = none_throws(
            self._serial_port,
            "Tried to communicate with serial port without opening it",
        )
        serial_port.write(data)
        return serial_port.readline().decode("utf-8")


elegoo_mars = ElegooMars()
elegoo_mars.open()
print(f"Firmware Version: {elegoo_mars.get_firmware_version()}")
print(f"State: {elegoo_mars.get_state()}")
elegoo_mars.close()
