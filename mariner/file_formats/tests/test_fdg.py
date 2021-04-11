import hashlib
import io
import pathlib
from unittest import TestCase

import png
from pyexpect import expect

from mariner.file_formats.fdg import FDGFile


class FDGFileTest(TestCase):
    def test_loading_fdg_file(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.fdg"
        fdg_file = FDGFile.read(path)
        expect(fdg_file.filename).to_equal("stairs.fdg")
        expect(fdg_file.bed_size_mm).to_equal((82.62, 130.56, 155.0))
        expect(fdg_file.height_mm).close_to(20.0, max_delta=1e-9)
        expect(fdg_file.layer_height_mm).close_to(0.05, max_delta=1e-9)
        expect(fdg_file.layer_count).to_equal(400)
        expect(fdg_file.resolution).to_equal((1620, 2560))
        expect(fdg_file.print_time_secs).to_equal(4243)
        expect(fdg_file.end_byte_offset_by_layer[:5]).to_equal(
            [78407, 120241, 162075, 203909, 245743]
        )
        expect(fdg_file.end_byte_offset_by_layer[-5:]).to_equal(
            [16704074, 16747148, 16790222, 16833296, 16876370]
        )
        expect(fdg_file.slicer_version).to_equal("1.8.1.0")
        expect(fdg_file.printer_name).to_equal("Voxelab Proxima 6")

    def test_preview_rendering(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.fdg"
        bytes = io.BytesIO()
        preview_image: png.Image = FDGFile.read_preview(path)
        preview_image.write(bytes)
        expect(preview_image.info["width"]).to_equal(400)
        expect(preview_image.info["height"]).to_equal(300)
        expect(preview_image.info["bitdepth"]).to_equal(5)
        expect(preview_image.info["alpha"]).is_false()
        expect(hashlib.md5(bytes.getvalue()).hexdigest()).to_equal(
            "8d83ad0d68d29f3a1fddce251c061782"
        )
