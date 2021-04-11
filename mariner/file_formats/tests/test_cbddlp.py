import hashlib
import io
import pathlib
from unittest import TestCase

import png
from pyexpect import expect

from mariner.file_formats.cbddlp import CBDDLPFile


class CBDDLPFileTest(TestCase):
    def test_loading_cbddlp_file(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "pyramid.cbddlp"
        cbddlp_file = CBDDLPFile.read(path)
        expect(cbddlp_file.filename).to_equal("pyramid.cbddlp")
        expect(cbddlp_file.bed_size_mm).to_equal((68.04, 120.96, 150.0))
        expect(cbddlp_file.height_mm).close_to(2.5, max_delta=1e-9)
        expect(cbddlp_file.layer_height_mm).close_to(0.05, max_delta=1e-9)
        expect(cbddlp_file.layer_count).to_equal(50)
        expect(cbddlp_file.resolution).to_equal((1440, 2560))
        expect(cbddlp_file.print_time_secs).to_equal(931)
        expect(cbddlp_file.end_byte_offset_by_layer[:5]).to_equal(
            [42047, 161261, 280467, 399665, 518853]
        )
        expect(cbddlp_file.end_byte_offset_by_layer[-5:]).to_equal(
            [5389468, 5507868, 5626244, 5744596, 5862924]
        )
        expect(cbddlp_file.slicer_version).to_equal("1.7.0.0")
        expect(cbddlp_file.printer_name).to_equal("ELEGOO MARS")

    def test_preview_rendering(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "pyramid.cbddlp"
        bytes = io.BytesIO()
        preview_image: png.Image = CBDDLPFile.read_preview(path)
        preview_image.write(bytes)
        expect(preview_image.info["width"]).to_equal(400)
        expect(preview_image.info["height"]).to_equal(300)
        expect(preview_image.info["bitdepth"]).to_equal(5)
        expect(preview_image.info["alpha"]).is_false()
        expect(hashlib.md5(bytes.getvalue()).hexdigest()).to_equal(
            "1e80ffc6bd1e975f9c943dfbcb990be5"
        )
