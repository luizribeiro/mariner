import pathlib
import struct
from dataclasses import dataclass
from typing import List

import png
from typedstruct import LittleEndianStruct, StructType

from mariner.file_formats import SlicedModelFile


@dataclass(frozen=True)
class FDGHeader(LittleEndianStruct):
    magic: int = StructType.uint32()
    version: int = StructType.uint32()
    layer_count: int = StructType.uint32()
    bottom_count: int = StructType.uint32()
    projector: int = StructType.uint32()
    bottom_layer_count: int = StructType.uint32()
    resolution_x: int = StructType.uint32()
    resolution_y: int = StructType.uint32()
    layer_height_mm: float = StructType.float32()
    layer_exposure: float = StructType.float32()
    bottom_exposure: float = StructType.float32()
    high_res_preview_offset: int = StructType.uint32()
    low_res_preview_offset: int = StructType.uint32()
    layer_defs_offset: int = StructType.uint32()
    print_time: int = StructType.uint32()
    anti_alias_level: int = StructType.uint32()
    light_pwm: int = StructType.uint16()
    bottom_light_pwm: int = StructType.uint16()
    unknown_00: int = StructType.uint32()
    unknown_01: int = StructType.uint32()
    height_mm: float = StructType.float32()
    bed_size_x_mm: float = StructType.float32()
    bed_size_y_mm: float = StructType.float32()
    bed_size_z_mm: float = StructType.float32()
    encryption_seed: int = StructType.uint32()
    anti_alias_depth: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    volume_milliliters: float = StructType.float32()
    weight_grams: float = StructType.float32()
    cost_dollars: float = StructType.float32()
    machine_offset: int = StructType.uint32()
    machine_size: int = StructType.uint32()
    bottom_light_off_time: float = StructType.float32()
    light_off_time: float = StructType.float32()
    unknown_03: int = StructType.uint32()
    bottom_lift_height: float = StructType.float32()
    bottom_lift_speed: float = StructType.float32()
    lift_height: float = StructType.float32()
    lift_speed: float = StructType.float32()
    retract_speed: float = StructType.float32()
    unknown_04: int = StructType.uint32()
    unknown_05: int = StructType.uint32()
    unknown_06: int = StructType.uint32()
    unknown_07: int = StructType.uint32()
    unknown_08: int = StructType.uint32()
    unknown_09: int = StructType.uint32()
    unknown_10: int = StructType.uint32()
    timestamp: int = StructType.uint32()
    slicer_version_patch: int = StructType.unsigned_char()
    slicer_version_minor: int = StructType.unsigned_char()
    slicer_version_major: int = StructType.unsigned_char()
    slicer_version_release: int = StructType.unsigned_char()
    unknown_11: int = StructType.uint32()
    unknown_12: int = StructType.uint32()
    unknown_13: int = StructType.uint32()
    unknown_14: int = StructType.uint32()
    unknown_15: int = StructType.uint32()
    unknown_16: int = StructType.uint32()


@dataclass(frozen=True)
class FDGLayerDef(LittleEndianStruct):
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
class FDGPreview(LittleEndianStruct):
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
class FDGFile(SlicedModelFile):
    @classmethod
    def read(self, path: pathlib.Path) -> "FDGFile":
        with open(str(path), "rb") as file:
            fdg_header = FDGHeader.unpack(file.read(FDGHeader.get_size()))

            file.seek(fdg_header.machine_offset)
            printer_name = file.read(fdg_header.machine_size).decode()

            end_byte_offset_by_layer = []
            for layer in range(0, fdg_header.layer_count):
                file.seek(fdg_header.layer_defs_offset + layer * FDGLayerDef.get_size())
                layer_def = FDGLayerDef.unpack(file.read(FDGLayerDef.get_size()))
                end_byte_offset_by_layer.append(
                    layer_def.image_offset + layer_def.image_length
                )

            return FDGFile(
                filename=path.name,
                bed_size_mm=(
                    round(fdg_header.bed_size_x_mm, 4),
                    round(fdg_header.bed_size_y_mm, 4),
                    round(fdg_header.bed_size_z_mm, 4),
                ),
                height_mm=fdg_header.height_mm,
                layer_height_mm=fdg_header.layer_height_mm,
                layer_count=fdg_header.layer_count,
                resolution=(fdg_header.resolution_x, fdg_header.resolution_y),
                print_time_secs=fdg_header.print_time,
                end_byte_offset_by_layer=end_byte_offset_by_layer,
                slicer_version=".".join(
                    [
                        str(fdg_header.slicer_version_release),
                        str(fdg_header.slicer_version_major),
                        str(fdg_header.slicer_version_minor),
                        str(fdg_header.slicer_version_patch),
                    ]
                ),
                printer_name=printer_name,
            )

    @classmethod
    def read_preview(cls, path: pathlib.Path) -> png.Image:
        with open(str(path), "rb") as file:
            fdg_header = FDGHeader.unpack(file.read(FDGHeader.get_size()))

            file.seek(fdg_header.high_res_preview_offset)
            preview = FDGPreview.unpack(file.read(FDGPreview.get_size()))

            file.seek(preview.image_offset)
            data = file.read(preview.image_length)

            return _read_image(preview.resolution_x, preview.resolution_y, data)
