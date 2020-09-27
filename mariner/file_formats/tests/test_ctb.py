import hashlib
import io
import pathlib
from unittest import TestCase

import png
from pyexpect import expect

from mariner.file_formats.ctb import CTBFile


class CTBFileTest(TestCase):
    def test_loading_ctb_file(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.ctb"
        ctb_file = CTBFile.read(path)
        expect(ctb_file.filename).to_equal("stairs.ctb")
        expect(ctb_file.bed_size_mm).to_equal((68.04, 120.96, 150.0))
        expect(ctb_file.height_mm).close_to(20.0, max_delta=1e-9)
        expect(ctb_file.layer_height_mm).close_to(0.05, max_delta=1e-9)
        expect(ctb_file.layer_count).to_equal(400)
        expect(ctb_file.resolution).to_equal((1440, 2560))
        expect(ctb_file.print_time_secs).to_equal(5621)
        expect(ctb_file.end_byte_offset_by_layer[:5]).to_equal(
            [26272, 28057, 29842, 31627, 33412]
        )
        expect(ctb_file.end_byte_offset_by_layer[-5:]).to_equal(
            [822027, 824704, 827383, 830061, 832745]
        )

    def test_preview_rendering(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.ctb"
        bytes = io.BytesIO()
        preview_image: png.Image = CTBFile.read_preview(path)
        preview_image.write(bytes)
        expect(preview_image.info["width"]).to_equal(400)
        expect(preview_image.info["height"]).to_equal(300)
        expect(preview_image.info["bitdepth"]).to_equal(5)
        expect(preview_image.info["alpha"]).is_false()
        expect(hashlib.md5(bytes.getvalue()).hexdigest()).to_equal(
            "ca98c806d42898ba70626e556f714928"
        )
