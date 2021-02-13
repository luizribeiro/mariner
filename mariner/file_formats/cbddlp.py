import pathlib
import struct
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import png
from typedstruct import LittleEndianStruct, StructType


@dataclass(frozen=True)
class CBDDLPHeader(LittleEndianStruct):
    magic: int = StructType.uint32()
    version: int = StructType.uint32()
    bed_size_x_mm: float = StructType.float32()
    bed_size_y_mm: float = StructType.float32()
    bed_size_z_mm: float = StructType.float32()
    unknown_01: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    height_mm: float = StructType.float32()
    layer_height_mm: float = StructType.float32()
    layer_exposure: float = StructType.float32()
    bottom_exposure: float = StructType.float32()
    layer_off_time: float = StructType.float32()
    bottom_count: int = StructType.uint32()
    resolution_x: int = StructType.uint32()
    resolution_y: int = StructType.uint32()
    high_res_preview_offset: int = StructType.uint32()
    layer_defs_offset: int = StructType.uint32()
    layer_count: int = StructType.uint32()
    low_res_preview_offset: int = StructType.uint32()
    print_time: int = StructType.uint32()
    projector: int = StructType.uint32()
    param_offset: int = StructType.uint32()
    param_size: int = StructType.uint32()
    anti_alias_level: int = StructType.uint32()
    light_pwm: int = StructType.uint16()
    bottom_light_pwm: int = StructType.uint16()
    encryption_seed: int = StructType.uint32()
    slicer_offset: int = StructType.uint32()
    slicer_size: int = StructType.uint32()


@dataclass(frozen=True)
class CBDDLPSlicer(LittleEndianStruct):
    skip_0: int = StructType.uint32()
    skip_1: int = StructType.uint32()
    skip_2: int = StructType.uint32()
    skip_3: int = StructType.uint32()
    skip_4: int = StructType.uint32()
    skip_5: int = StructType.uint32()
    skip_6: int = StructType.uint32()
    machine_offset: int = StructType.uint32()
    machine_size: int = StructType.uint32()
    encryption_mode: int = StructType.uint32()
    time_seconds: int = StructType.uint32()
    unknown_01: int = StructType.uint32()
    version_patch: int = StructType.unsigned_char()
    version_minor: int = StructType.unsigned_char()
    version_major: int = StructType.unsigned_char()
    version_release: int = StructType.unsigned_char()
    unknown_02: int = StructType.uint32()
    unknown_03: int = StructType.uint32()
    unknown_04: float = StructType.float32()
    unknown_05: int = StructType.uint32()
    unknown_06: int = StructType.uint32()
    unknown_07: float = StructType.float32()


@dataclass(frozen=True)
class CBDDLPLayerDef(LittleEndianStruct):
    layer_height_mm: float = StructType.float32()
    layer_exposure: float = StructType.float32()
    layer_off_time: float = StructType.float32()
    image_offset: int = StructType.uint32()
    image_length: int = StructType.uint32()
    unknown_01: int = StructType.uint32()
    image_info_size: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    unknown_03: int = StructType.uint32()


@dataclass(frozen=True)
class CBDDLPPreview(LittleEndianStruct):
    resolution_x: int = StructType.uint32()
    resolution_y: int = StructType.uint32()
    image_offset: int = StructType.uint32()
    image_length: int = StructType.uint32()


REPEAT_RGB15_MASK: int = 1 << 5


def _read_image(width: int, height: int, data: bytes) -> png.Image:
    array: List[List[int]] = [[]]

    (i, x) = (0, 0)
    while i < len(data):
        color16 = int(struct.unpack_from("<H", data, i)[0])
        i += 2
        repeat = 1
        if color16 & REPEAT_RGB15_MASK:
            repeat += int(struct.unpack_from("<H", data, i)[0]) & 0xFFF
            i += 2

        (r, g, b) = (
            (color16 >> 0) & 0x1F,
            (color16 >> 6) & 0x1F,
            (color16 >> 11) & 0x1F,
        )

        while repeat > 0:
            array[-1] += [r, g, b]
            repeat -= 1

            x += 1
            if x == width:
                x = 0
                array.append([])

    array.pop()

    return png.from_array(array, "RGB;5")


@dataclass(frozen=True)
class CBDDLPFile:
    filename: str
    bed_size_mm: Tuple[float, float, float]
    height_mm: float
    layer_height_mm: float
    layer_count: int
    resolution: Tuple[int, int]
    print_time_secs: int
    end_byte_offset_by_layer: Sequence[int]
    slicer_version: str
    printer_name: str

    @classmethod
    def read(self, path: pathlib.Path) -> "CBDDLPFile":
        with open(str(path), "rb") as file:
            CBDDLP_header = CBDDLPHeader.unpack(file.read(CBDDLPHeader.get_size()))

            file.seek(CBDDLP_header.slicer_offset)
            CBDDLP_slicer = CBDDLPSlicer.unpack(file.read(CBDDLPSlicer.get_size()))

            file.seek(CBDDLP_slicer.machine_offset)
            printer_name = file.read(CBDDLP_slicer.machine_size).decode()

            end_byte_offset_by_layer = []
            for layer in range(0, CBDDLP_header.layer_count):
                file.seek(CBDDLP_header.layer_defs_offset + layer * CBDDLPLayerDef.get_size())
                layer_def = CBDDLPLayerDef.unpack(file.read(CBDDLPLayerDef.get_size()))
                end_byte_offset_by_layer.append(
                    layer_def.image_offset + layer_def.image_length
                )

            return CBDDLPFile(
                filename=path.name,
                bed_size_mm=(
                    round(CBDDLP_header.bed_size_x_mm, 4),
                    round(CBDDLP_header.bed_size_y_mm, 4),
                    round(CBDDLP_header.bed_size_z_mm, 4),
                ),
                height_mm=CBDDLP_header.height_mm,
                layer_height_mm=CBDDLP_header.layer_height_mm,
                layer_count=CBDDLP_header.layer_count,
                resolution=(CBDDLP_header.resolution_x, CBDDLP_header.resolution_y),
                print_time_secs=CBDDLP_header.print_time,
                end_byte_offset_by_layer=end_byte_offset_by_layer,
                slicer_version=".".join(
                    [
                        str(CBDDLP_slicer.version_release),
                        str(CBDDLP_slicer.version_major),
                        str(CBDDLP_slicer.version_minor),
                        str(CBDDLP_slicer.version_patch),
                    ]
                ),
                printer_name=printer_name,
            )

    @classmethod
    def read_preview(cls, path: pathlib.Path) -> png.Image:
        with open(str(path), "rb") as file:
            CBDDLP_header = CBDDLPHeader.unpack(file.read(CBDDLPHeader.get_size()))

            file.seek(CBDDLP_header.high_res_preview_offset)
            preview = CBDDLPPreview.unpack(file.read(CBDDLPPreview.get_size()))

            file.seek(preview.image_offset)
            data = file.read(preview.image_length)

            return _read_image(preview.resolution_x, preview.resolution_y, data)