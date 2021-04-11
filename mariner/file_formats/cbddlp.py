from typing import Type

from mariner.file_formats import SlicedModelFile
from mariner.file_formats.ctb import CTBFile


# we just treat cbddlp as a ctb file, since they're very similar to each other
CBDDLPFile: Type[SlicedModelFile] = CTBFile
