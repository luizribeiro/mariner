import pathlib
from unittest import TestCase
from unittest.mock import call, patch, MagicMock

from mariner.server import CacheBootstrapper


class CacheBootstrapperTest(TestCase):
    @patch("mariner.server.read_cached_sliced_model_file")
    @patch("mariner.server.read_cached_preview")
    def test_ctb_metadata_cache(
        self,
        read_cached_preview_mock: MagicMock,
        read_cached_sliced_model_file_mock: MagicMock,
    ) -> None:
        files_directory = (
            pathlib.Path(__file__).parent.parent.absolute() / "file_formats" / "tests"
        )

        with patch("mariner.config.get_files_directory", return_value=files_directory):
            CacheBootstrapper().run()

        read_cached_sliced_model_file_mock.assert_has_calls(
            [
                call(files_directory / "stairs.fdg"),
                call(files_directory / "pyramid.cbddlp"),
                call(files_directory / "stairs.ctb"),
            ],
            any_order=True,
        )

        read_cached_preview_mock.assert_has_calls(
            [
                call(files_directory / "stairs.fdg"),
                call(files_directory / "pyramid.cbddlp"),
                call(files_directory / "stairs.ctb"),
            ],
            any_order=True,
        )
