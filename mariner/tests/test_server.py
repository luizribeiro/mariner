import hashlib
import io
import os
import pathlib
from unittest.mock import patch, ANY, Mock

from freezegun import freeze_time
from pyexpect import expect
from pyfakefs.fake_filesystem_unittest import TestCase
from werkzeug.datastructures import FileStorage

from mariner import config
from mariner.exceptions import UnexpectedPrinterResponse
from mariner.printer import (
    ChiTuPrinter,
    PrinterState,
    PrintStatus,
)
from mariner.server.app import app
from mariner.server.utils import read_cached_sliced_model_file


class MarinerServerTest(TestCase):
    def setUp(self) -> None:
        path = (
            pathlib.Path(__file__).parent.parent.absolute()
            / "file_formats"
            / "tests"
            / "stairs.ctb"
        )
        with open(path, "rb") as file:
            self.ctb_file_contents = file.read()

        forkpath = (
            pathlib.Path(__file__)
            .parent.parent.absolute()
            .joinpath("file_formats", "tests", "._stairs.ctb")
        )
        with open(forkpath, "rb") as forkfile:
            self.fork_file_contents = forkfile.read()

        self.setUpPyfakefs()
        self.fs.create_file(
            "/mnt/usb_share/foobar.ctb", contents=self.ctb_file_contents
        )
        self.fs.create_file(
            "/mnt/usb_share/._foobar.ctb", contents=self.fork_file_contents
        )

        self.client = app.test_client()
        app.config["WTF_CSRF_ENABLED"] = False

        self.printer_mock = Mock(spec=ChiTuPrinter)
        self.printer_patcher = patch("mariner.server.api.ChiTuPrinter")
        printer_constructor_mock = self.printer_patcher.start()
        printer_constructor_mock.return_value = self.printer_mock
        self.printer_mock.__enter__ = Mock(return_value=self.printer_mock)
        self.printer_mock.__exit__ = Mock(return_value=None)

        # this is so we don't try caching the values returned by this function during
        # tests. this is important because during tests this function returns a Mock,
        # which pickle cannot serialize.
        self._read_ctb_file_patcher = patch(
            "mariner.server.api.read_cached_sliced_model_file",
            side_effect=read_cached_sliced_model_file.__wrapped__,
        )
        self._read_ctb_file_patcher.start()

    def tearDown(self) -> None:
        self.printer_patcher.stop()

    def test_print_status_while_printing(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.PRINTING,
            current_byte=256537,
            total_bytes=832745,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "PRINTING",
                "selected_file": "foobar.ctb",
                "progress": 32.25,
                "layer_count": 400,
                "current_layer": 130,
                "print_time_secs": 5621,
                "time_left_secs": 3808,
            }
        )

    def test_print_status_when_paused(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.PAUSED,
            current_byte=256537,
            total_bytes=832745,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "PAUSED",
                "selected_file": "foobar.ctb",
                "progress": 32.25,
                "layer_count": 400,
                "current_layer": 130,
                "print_time_secs": 5621,
                "time_left_secs": 3808,
            }
        )

    def test_print_status_while_starting_print(self) -> None:
        self.printer_mock.get_selected_file.return_value = "foobar.ctb"
        self.printer_mock.get_print_status.return_value = PrintStatus(
            state=PrinterState.STARTING_PRINT,
            current_byte=0,
            total_bytes=832745,
        )
        response = self.client.get("/api/print_status")
        expect(response.get_json()).to_equal(
            {
                "state": "STARTING_PRINT",
                "selected_file": "foobar.ctb",
                "progress": 0.0,
                "layer_count": 400,
                "current_layer": 1,
                "print_time_secs": 5621,
                "time_left_secs": 5621,
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

    def test_list_files(self) -> None:
        self.fs.create_dir("/mnt/usb_share/subdir/")
        with freeze_time("2020-03-15"):
            self.fs.create_file("/mnt/usb_share/a.ctb", contents=self.ctb_file_contents)
        with freeze_time("2020-03-17"):
            self.fs.create_file("/mnt/usb_share/b.ctb", contents=self.ctb_file_contents)
        with freeze_time("2020-03-16"):
            self.fs.create_file(
                "/mnt/usb_share/random_file.txt", contents="dummy content"
            )
        with freeze_time("2021-05-14"):
            self.fs.create_file(
                "/mnt/usb_share/README",
                contents=self.ctb_file_contents,
            )
        with freeze_time("2021-05-15"):
            self.fs.create_file(
                "/mnt/usb_share/case.CtB",
                contents=self.ctb_file_contents,
            )

        response = self.client.get("/api/list_files")
        expect(response.get_json()).to_equal(
            {
                "directories": [{"dirname": "subdir"}],
                "files": [
                    {
                        "filename": "._foobar.ctb",
                        "path": "._foobar.ctb",
                        "can_be_printed": False,
                    },
                    {
                        "filename": "foobar.ctb",
                        "path": "foobar.ctb",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
                    {
                        "filename": "case.CtB",
                        "path": "case.CtB",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
                    {
                        "filename": "README",
                        "path": "README",
                        "can_be_printed": False,
                    },
                    {
                        "filename": "b.ctb",
                        "path": "b.ctb",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
                    {
                        "filename": "random_file.txt",
                        "path": "random_file.txt",
                        "can_be_printed": False,
                    },
                    {
                        "filename": "a.ctb",
                        "path": "a.ctb",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
                ],
            }
        )

    def test_list_files_under_subdirectory(self) -> None:
        self.fs.create_dir("/mnt/usb_share/foo/bar/subdir/")
        self.fs.create_file(
            "/mnt/usb_share/foo/bar/a.ctb", contents=self.ctb_file_contents
        )
        self.fs.create_file(
            "/mnt/usb_share/foo/bar/b.ctb", contents=self.ctb_file_contents
        )

        response = self.client.get("/api/list_files?path=foo/bar/")
        expect(response.get_json()).to_equal(
            {
                "directories": [{"dirname": "subdir"}],
                "files": [
                    {
                        "filename": "b.ctb",
                        "path": "foo/bar/b.ctb",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
                    {
                        "filename": "a.ctb",
                        "path": "foo/bar/a.ctb",
                        "print_time_secs": 5621,
                        "can_be_printed": True,
                    },
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

    def test_error_handling_while_stopping_print(self) -> None:
        self.printer_mock.stop_printing.side_effect = UnexpectedPrinterResponse(
            "foobar\r\n"
        )
        response = self.client.post("/api/printer/command/cancel_print")
        expect(response.status_code).to_equal(500)
        expect(response.get_json()).to_equal(
            {
                "title": "Unexpected Printer Response",
                "description": "The printer returned an unexpected response: "
                + "'foobar\\r\\n'",
                "traceback": ANY,
            }
        )
        self.printer_mock.stop_printing.assert_called_once_with()

    def test_command_reboot(self) -> None:
        response = self.client.post("/api/printer/command/reboot")
        expect(response.get_json()).to_equal({"success": True})
        self.printer_mock.reboot.assert_called_once_with()

    def test_file_details(self) -> None:
        response = self.client.get("/api/file_details?filename=foobar.ctb")
        expect(response.get_json()).to_equal(
            {
                "filename": "foobar.ctb",
                "path": "foobar.ctb",
                "bed_size_mm": [68.04, 120.96, 150.0],
                "height_mm": 20.0,
                "layer_count": 400,
                "layer_height_mm": 0.05,
                "resolution": [1440, 2560],
                "print_time_secs": 5621,
            }
        )

    def test_file_details_in_subdirectory(self) -> None:
        self.fs.create_file(
            "/mnt/usb_share/functional/stairs.ctb", contents=self.ctb_file_contents
        )

        response = self.client.get("/api/file_details?filename=functional/stairs.ctb")
        expect(response.get_json()).to_equal(
            {
                "filename": "stairs.ctb",
                "path": "functional/stairs.ctb",
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
        response = self.client.get("/api/file_preview?filename=foobar.ctb")
        expect(response.content_type).to_equal("image/png")
        expect(hashlib.md5(response.get_data()).hexdigest()).to_equal(
            "ca98c806d42898ba70626e556f714928"
        )

    def test_file_preview_with_invalid_path(self) -> None:
        response = self.client.get("/api/file_preview?filename=../../etc/passwd")
        expect(response.status_code).to_equal(400)

    def test_upload_file_without_a_file(self) -> None:
        response = self.client.post("/api/upload_file")
        expect(response.status_code).to_equal(400)

    def test_upload_file_with_an_empty_filename(self) -> None:
        data = {"file": (io.BytesIO(b"abcdef"), "")}
        response = self.client.post("/api/upload_file", data=data)
        expect(response.status_code).to_equal(400)

    def test_upload_file_with_an_unsupported_file_extension(self) -> None:
        data = {"file": (io.BytesIO(b"abcdef"), "image.jpg")}
        response = self.client.post("/api/upload_file", data=data)
        expect(response.status_code).to_equal(400)

    def test_upload_file(self) -> None:
        data = {"file": (io.BytesIO(b"abcdef"), "myfile.ctb")}
        with patch.object(FileStorage, "save") as save_file_mock:
            response = self.client.post("/api/upload_file", data=data)
        expect(response.status_code).to_equal(200)
        expect(response.get_json()).to_equal({"success": True})
        save_file_mock.assert_called_once_with(
            str(config.get_files_directory() / "myfile.ctb")
        )

    def test_upload_file_with_upper_case_extension(self) -> None:
        data = {"file": (io.BytesIO(b"abcdef"), "myfile.CtB")}
        with patch.object(FileStorage, "save") as save_file_mock:
            response = self.client.post("/api/upload_file", data=data)
        expect(response.status_code).to_equal(200)
        expect(response.get_json()).to_equal({"success": True})
        save_file_mock.assert_called_once_with(
            str(config.get_files_directory() / "myfile.CtB")
        )

    def test_upload_file_with_sanitized_file(self) -> None:
        data = {"file": (io.BytesIO(b"abcdef"), "../../../etc/passwd.ctb")}
        with patch.object(FileStorage, "save") as save_file_mock:
            response = self.client.post("/api/upload_file", data=data)
        expect(response.status_code).to_equal(200)
        expect(response.get_json()).to_equal({"success": True})
        save_file_mock.assert_called_once_with(
            str(config.get_files_directory() / "etc_passwd.ctb")
        )

    def test_delete_file(self) -> None:
        expect(os.path.exists(config.get_files_directory() / "mariner.ctb")).to_equal(
            False
        )
        self.fs.create_file(
            "/mnt/usb_share/mariner.ctb", contents=self.ctb_file_contents
        )
        expect(os.path.exists(config.get_files_directory() / "mariner.ctb")).to_equal(
            True
        )

        response = self.client.post("/api/delete_file?filename=mariner.ctb")
        expect(response.status_code).to_equal(200)
        expect(response.get_json()).to_equal({"success": True})
        expect(os.path.exists(config.get_files_directory() / "mariner.ctb")).to_equal(
            False
        )

    def test_delete_file_that_is_not_file(self) -> None:
        with patch("os.remove") as remove_mock:
            response = self.client.post("/api/delete_file?filename=mariner")
        remove_mock.assert_not_called()
        expect(response.status_code).to_equal(400)

    def test_delete_file_with_invalid_path(self) -> None:
        response = self.client.post("/api/delete_file?filename=../../etc/passwd")
        expect(response.status_code).to_equal(400)

    def test_get_index(self) -> None:
        with patch(
            "mariner.server.render_template", return_value=""
        ) as render_template_mock:
            response = self.client.get("/")
            render_template_mock.assert_called_with(
                "index.html",
                supported_extensions=ANY,
            )
        expect(response.status_code).to_equal(200)
