from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock

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
        response = self.client.get("/api/print_status")
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
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "selected_file": "foobar.ctb",
                "is_printing": False,
                "progress": 0.0,
            }
        )

    @patch("mariner.server.os.listdir", return_value=["a.ctb", "b.ctb"])
    def test_list_files(self, _list_dir_mock: MagicMock) -> None:
        response = self.client.get("/api/list_files")
        expect(response.get_json()).to_equal(
            {
                "files": [{"filename": "a.ctb"}, {"filename": "b.ctb"}],
            }
        )

    def test_command_start_printing(self) -> None:
        response = self.client.post(
            "/api/printer/command/start_print?filename=foobar.ctb"
        )
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.select_file.assert_called_once_with("foobar.ctb")
        self.printer_mock.start_printing.assert_called_once_with()

    def test_command_pause_print(self) -> None:
        response = self.client.post("/api/printer/command/pause_print")
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.pause_printing.assert_called_once_with()

    def test_command_resume_print(self) -> None:
        response = self.client.post("/api/printer/command/resume_print")
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.resume_printing.assert_called_once_with()

    def test_command_cancel_print(self) -> None:
        response = self.client.post("/api/printer/command/cancel_print")
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.stop_printing.assert_called_once_with()

    def test_command_reboot(self) -> None:
        response = self.client.post("/api/printer/command/reboot")
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.reboot.assert_called_once_with()
