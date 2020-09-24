import pathlib
from unittest import TestCase

from pyexpect import expect

from mariner.file_formats.ctb import CTBFile


class CTBFileTest(TestCase):
    def test_loading_ctb_file(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.ctb"
        ctb_file = CTBFile.read(str(path))
        expect(ctb_file.height_mm).close_to(20.0, max_delta=1e-9)
        expect(ctb_file.layer_height).close_to(0.05, max_delta=1e-9)
        expect(ctb_file.layer_count).to_equal(400)
        expect(ctb_file.print_time_secs).to_equal(5621)
        expect(ctb_file.end_byte_offset_by_layer[:5]).to_equal(
            [26272, 28057, 29842, 31627, 33412]
        )
        expect(ctb_file.end_byte_offset_by_layer[-5:]).to_equal(
            [822027, 824704, 827383, 830061, 832745]
        )
