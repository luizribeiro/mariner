import pathlib
from dataclasses import dataclass
from typing import Sequence

from typedstruct import LittleEndianStruct, StructType


@dataclass(frozen=True)
class CTBHeader(LittleEndianStruct):
    magic: int = StructType.uint32()
    version: int = StructType.uint32()
    bed_size_x_mm: float = StructType.float32()
    bed_size_y_mm: float = StructType.float32()
    bed_size_z_mm: float = StructType.float32()
    unknown_01: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    height_mm: float = StructType.float32()
    layer_height: float = StructType.float32()
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


@dataclass(frozen=True)
class CTBLayerDef(LittleEndianStruct):
    layer_height: float = StructType.float32()
    layer_exposure: float = StructType.float32()
    layer_off_time: float = StructType.float32()
    image_offset: int = StructType.uint32()
    image_length: int = StructType.uint32()
    unknown_01: int = StructType.uint32()
    image_info_size: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    unknown_03: int = StructType.uint32()


class CTBFile:
    def __init__(
        self,
        filename: str,
        height_mm: float,
        layer_height: float,
        layer_count: int,
        print_time_secs: int,
        end_byte_offset_by_layer: Sequence[int],
    ) -> None:
        self.filename = filename
        self.height_mm = height_mm
        self.layer_height = layer_height
        self.layer_count = layer_count
        self.print_time_secs = print_time_secs
        self.end_byte_offset_by_layer = end_byte_offset_by_layer

    @classmethod
    def read(self, path: pathlib.Path) -> "CTBFile":
        with open(str(path), "rb") as file:
            ctb_header = CTBHeader.unpack(file.read(CTBHeader.get_size()))

            end_byte_offset_by_layer = []
            for layer in range(0, ctb_header.layer_count):
                file.seek(ctb_header.layer_defs_offset + layer * CTBLayerDef.get_size())
                layer_def = CTBLayerDef.unpack(file.read(CTBLayerDef.get_size()))
                end_byte_offset_by_layer.append(
                    layer_def.image_offset + layer_def.image_length
                )

            return CTBFile(
                filename=path.name,
                height_mm=ctb_header.height_mm,
                layer_height=ctb_header.layer_height,
                layer_count=ctb_header.layer_count,
                print_time_secs=ctb_header.print_time,
                end_byte_offset_by_layer=end_byte_offset_by_layer,
            )
