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

    def test_can_customize_files_directory(self) -> None:
        self.fs.create_file(
            "/etc/mariner/config.toml",
            contents="""
files_directory = "/var/mariner"
            """,
        )
        expect(config.get_files_directory()).to_equal(Path("/var/mariner"))
