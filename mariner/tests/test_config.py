from pathlib import Path

from pyexpect import expect
from pyfakefs.fake_filesystem_unittest import TestCase

from mariner import config


class ConfigurationTest(TestCase):
    def setUp(self) -> None:
        config._get_config.cache_clear()
        self.setUpPyfakefs()

    def test_default_values(self) -> None:
        expect(config.get_files_directory()).to_equal(Path("/mnt/usb_share"))

        expect(config.get_printer_display_name()).to_equal(None)
        expect(config.get_printer_serial_port()).to_equal("/dev/serial0")
        expect(config.get_printer_baudrate()).to_equal(115200)

        expect(config.get_http_host()).to_equal("0.0.0.0")
        expect(config.get_http_port()).to_equal(5050)

        expect(config.get_cache_directory()).to_equal("/tmp/mariner/")

    def test_can_customize_files_directory(self) -> None:
        self.fs.create_file(
            "/etc/mariner/config.toml",
            contents="""
files_directory = "/var/mariner"
            """,
        )
        expect(config.get_files_directory()).to_equal(Path("/var/mariner"))

    def test_can_customize_printer_settings(self) -> None:
        self.fs.create_file(
            "/etc/mariner/config.toml",
            contents="""
[printer]
display_name = "Elegoo Mars"
serial_port = "/dev/ttyUSB0"
baudrate = 9600
            """,
        )
        expect(config.get_printer_display_name()).to_equal("Elegoo Mars")
        expect(config.get_printer_serial_port()).to_equal("/dev/ttyUSB0")
        expect(config.get_printer_baudrate()).to_equal(9600)

    def test_can_customize_http_settings(self) -> None:
        self.fs.create_file(
            "/etc/mariner/config.toml",
            contents="""
[http]
host = "127.0.0.1"
port = 80
            """,
        )
        expect(config.get_http_host()).to_equal("127.0.0.1")
        expect(config.get_http_port()).to_equal(80)

    def test_can_customize_cache_settings(self) -> None:
        self.fs.create_file(
            "/etc/mariner/config.toml",
            contents="""
[cache]
directory = "/dev/shm/mariner/"
            """,
        )
        expect(config.get_cache_directory()).to_equal("/dev/shm/mariner/")
