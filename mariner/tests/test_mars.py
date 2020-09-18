import unittest.mock
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mariner.mars import ElegooMars


class ElegooMarsTest(TestCase):
    printer: ElegooMars
    serial_port_patcher: unittest.mock._patch
    serial_port_mock: MagicMock

    def setUp(self) -> None:
        self.printer = ElegooMars()
        self.serial_port_mock = MagicMock()
        self.serial_port_patcher = patch("mariner.mars.serial.Serial")
        serial_port_constructor = self.serial_port_patcher.start()
        serial_port_constructor.return_value = self.serial_port_mock

    def tearDown(self) -> None:
        self.serial_port_patcher.stop()

    def test_open_and_close(self) -> None:
        self.serial_port_mock.open.assert_not_called()
        self.serial_port_mock.close.assert_not_called()

        self.printer.open()
        self.serial_port_mock.open.assert_called_once_with()
        self.serial_port_mock.close.assert_not_called()
        self.serial_port_mock.reset_mock()

        self.printer.close()
        self.serial_port_mock.open.assert_not_called()
        self.serial_port_mock.close.assert_called_once_with()
