from unittest import TestCase
from unittest.mock import patch, Mock

from pyexpect import expect

from mariner.mars import ElegooMars, PrintStatus
from mariner.server import app


class MarinerServerTest(TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        self.printer_mock = Mock(spec=ElegooMars)
        self.printer_patcher = patch("mariner.server.ElegooMars")
        printer_constructor_mock = self.printer_patcher.start()
        printer_constructor_mock.return_value = self.printer_mock
        self.printer_mock.__enter__ = Mock(return_value=self.printer_mock)
        self.printer_mock.__exit__ = Mock(return_value=None)

    def tearDown(self) -> None:
        self.printer_patcher.stop()

    def test_print_status_while_printing(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            is_printing=True,
            current_byte=42,
            total_bytes=120,
        )
        response = self.client.get("/print_status")
        expect(response.get_json()).to_equal(
            {
                "selected_file": "foobar.ctb",
                "is_printing": True,
                "progress": 35.0,
            }
        )

    def test_print_status_while_idle(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            is_printing=False,
            current_byte=0,
            total_bytes=0,
        )
        response = self.client.get("/print_status")
        expect(response.get_json()).to_equal(
            {
                "selected_file": "foobar.ctb",
                "is_printing": False,
                "progress": 0.0,
            }
        )
