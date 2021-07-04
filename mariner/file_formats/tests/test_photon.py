import hashlib
import io
import pathlib
from unittest import TestCase

import png
from pyexpect import expect

from mariner.file_formats.photon import PhotonFile


class PhotonFileTest(TestCase):
    def test_loading_photon_file(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.photon"
        photon_file = PhotonFile.read(path)
        expect(photon_file.filename).to_equal("stairs.photon")
        expect(photon_file.bed_size_mm).to_equal((68.04, 120.96, 150.0))
        expect(photon_file.height_mm).close_to(17.0, max_delta=1e-9)
        expect(photon_file.layer_height_mm).close_to(0.05, max_delta=1e-9)
        expect(photon_file.layer_count).to_equal(340)
        expect(photon_file.resolution).to_equal((1440, 2560))
        expect(photon_file.print_time_secs).to_equal(5171)
        expect(photon_file.end_byte_offset_by_layer[:5]).to_equal(
            [54492, 85084, 115763, 146232, 176680]
        )
        expect(photon_file.end_byte_offset_by_layer[-5:]).to_equal(
            [10132550, 10162753, 10192956, 10223159, 10253362]
        )

        expect(photon_file.slicer_version).to_equal("1.7.0.0")
        expect(photon_file.printer_name).to_equal("AnyCubic Photon")

    def test_preview_rendering(self) -> None:
        path = pathlib.Path(__file__).parent.absolute() / "stairs.photon"
        bytes = io.BytesIO()
        preview_image: png.Image = PhotonFile.read_preview(path)
        preview_image.write(bytes)
        expect(preview_image.info["width"]).to_equal(400)
        expect(preview_image.info["height"]).to_equal(300)
        expect(preview_image.info["bitdepth"]).to_equal(5)
        expect(preview_image.info["alpha"]).is_false()
        expect(hashlib.md5(bytes.getvalue()).hexdigest()).to_equal(
            "44e523ed707f3dfcad8071fe46c537f3"
        )
