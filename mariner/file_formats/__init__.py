import pathlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence, Tuple

import png


@dataclass(frozen=True)
class SlicedModelFile(ABC):
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
    @abstractmethod
    def read(self, path: pathlib.Path) -> "SlicedModelFile":
        ...

    @classmethod
    @abstractmethod
    def read_preview(cls, path: pathlib.Path) -> png.Image:
        ...
