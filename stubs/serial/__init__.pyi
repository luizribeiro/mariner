from serial.serialutil import *
from serial.serialjava import Serial as Serial
from serial.serialposix import (
    PosixPollSerial as PosixPollSerial,
    VTIMESerial as VTIMESerial,
)
from typing import List

VERSION: str
protocol_handler_packages: List[str]

def serial_for_url(url: str, *args: object, **kwargs: object) -> Serial: ...
