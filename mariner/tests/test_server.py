import hashlib
import pathlib
from os import DirEntry
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock

from pyexpect import expect

from mariner.file_formats.ctb import CTBFile
from mariner.mars import ElegooMars, PrinterState, PrintStatus
from mariner.server import app, _read_ctb_file


class MarinerServerTest(TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

        self.printer_mock = Mock(spec=ElegooMars)
        self.printer_patcher = patch("mariner.server.ElegooMars")
        printer_constructor_mock = self.printer_patcher.start()
        printer_constructor_mock.return_value = self.printer_mock
        self.printer_mock.__enter__ = Mock(return_value=self.printer_mock)
        self.printer_mock.__exit__ = Mock(return_value=None)

        self.ctb_file_mock = Mock(spec=CTBFile)
        self.ctb_file_mock.layer_count = 19
        self.ctb_file_mock.print_time_secs = 200
        self.ctb_file_mock.end_byte_offset_by_layer = [
            (i + 1) * 6 for i in range(0, self.ctb_file_mock.layer_count)
        ]
        self.ctb_file_patcher = patch("mariner.server.CTBFile")
        ctb_file_class_mock = self.ctb_file_patcher.start()
        ctb_file_class_mock.read.return_value = self.ctb_file_mock

        # this is so we don't try caching the values returned by this function during
        # tests. this is important because during tests this function returns a Mock,
        # which pickle cannot serialize.
        self._read_ctb_file_patcher = patch(
            "mariner.server._read_ctb_file", side_effect=_read_ctb_file.__wrapped__
        )
        self._read_ctb_file_patcher.start()

    def tearDown(self) -> None:
        self.printer_patcher.stop()
        self.ctb_file_patcher.stop()

    def test_print_status_while_printing(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.PRINTING,
            current_byte=42,
            total_bytes=120,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "PRINTING",
                "selected_file": "foobar.ctb",
                "progress": 31.57894736842105,
                "layer_count": 19,
                "current_layer": 7,
                "print_time_secs": 200,
                "time_left_secs": 137,
            }
        )

    def test_print_status_when_paused(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.PAUSED,
            current_byte=42,
            total_bytes=120,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "PAUSED",
                "selected_file": "foobar.ctb",
                "progress": 31.57894736842105,
                "layer_count": 19,
                "current_layer": 7,
                "print_time_secs": 200,
                "time_left_secs": 137,
            }
        )

    def test_print_status_while_starting_print(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.STARTING_PRINT,
            current_byte=0,
            total_bytes=120,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "STARTING_PRINT",
                "selected_file": "foobar.ctb",
                "progress": 0.0,
                "layer_count": 19,
                "current_layer": 1,
                "print_time_secs": 200,
                "time_left_secs": 200,
            }
        )

    def test_print_status_while_idle(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.IDLE,
            current_byte=0,
            total_bytes=0,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "IDLE",
                "selected_file": "foobar.ctb",
                "progress": 0.0,
            }
        )

    @patch("mariner.server.os.scandir")
    def test_list_files(self, _scandir_mock: MagicMock) -> None:
        subdir = Mock(spec=DirEntry)
        subdir.name = "subdir"
        subdir.is_file.return_value = False
        subdir.is_dir.return_value = True
        a_ctb = Mock(spec=DirEntry)
        a_ctb.name = "a.ctb"
        a_ctb.is_file.return_value = True
        a_ctb.is_dir.return_value = False
        b_ctb = Mock(spec=DirEntry)
        b_ctb.name = "b.ctb"
        b_ctb.is_file.return_value = True
        a_ctb.is_dir.return_value = False

        _scandir_context_manager_mock = MagicMock()
        _scandir_context_manager_mock.__enter__().__iter__.return_value = [
            subdir,
            a_ctb,
            b_ctb,
        ]
        _scandir_mock.return_value = _scandir_context_manager_mock

        response = self.client.get("/api/list_files")
        expect(response.get_json()).to_equal(
            {
                "directories": [{"dirname": "subdir"}],
                "files": [
                    {"filename": "a.ctb", "print_time_secs": 200},
                    {"filename": "b.ctb", "print_time_secs": 200},
                ],
            }
        )

    def test_list_files_from_invalid_directory(self) -> None:
        response = self.client.get("/api/list_files?path=../foo/")
        expect(response.status_code).to_equal(400)

    def test_command_start_printing(self) -> None:
        response = self.client.post(
            "/api/printer/command/start_print?filename=foobar.ctb"
        )
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.start_printing.assert_called_once_with("foobar.ctb")

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

    def test_file_details(self) -> None:
        path = (
            pathlib.Path(__file__).parent.parent.absolute()
            / "file_formats"
            / "tests"
            / "stairs.ctb"
        )
        ctb_file = CTBFile.read(path)

        with patch("mariner.server.CTBFile.read", return_value=ctb_file):
            response = self.client.get("/api/file_details?filename=stairs.ctb")
            expect(response.get_json()).to_equal(
                {
                    "filename": "stairs.ctb",
                    "bed_size_mm": [68.04, 120.96, 150.0],
                    "height_mm": 20.0,
                    "layer_count": 400,
                    "layer_height_mm": 0.05,
                    "resolution": [1440, 2560],
                    "print_time_secs": 5621,
                }
            )

    def test_file_details_with_invalid_path(self) -> None:
        response = self.client.get("/api/file_details?filename=../../etc/passwd")
        expect(response.status_code).to_equal(400)

    def test_file_preview(self) -> None:
        path = (
            pathlib.Path(__file__).parent.parent.absolute()
            / "file_formats"
            / "tests"
            / "stairs.ctb"
        )
        ctb_preview = CTBFile.read_preview(path)

        with patch("mariner.server.CTBFile.read_preview", return_value=ctb_preview):
            response = self.client.get("/api/file_preview?filename=stairs.ctb")
            expect(response.content_type).to_equal("image/png")
            expect(hashlib.md5(response.get_data()).hexdigest()).to_equal(
                "ca98c806d42898ba70626e556f714928"
            )
