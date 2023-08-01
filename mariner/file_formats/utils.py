import os
from typing import Mapping, Set, Type

from mariner.file_formats import SlicedModelFile
from mariner.file_formats.ctb import CTBFile
from mariner.file_formats.cbddlp import CBDDLPFile
from mariner.file_formats.fdg import FDGFile
from mariner.file_formats.photon import PhotonFile
from mariner.file_formats.ctb_encrypted import check_encrypted
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

EXTENSION_TO_FILE_FORMAT: Mapping[str, Type[SlicedModelFile]] = {
    ".ctb": CTBFile,
    ".cbddlp": CBDDLPFile,
    ".fdg": FDGFile,
    ".photon": PhotonFile,
}


def get_file_extension(filename: str) -> str:
    (_, extension) = os.path.splitext(filename)
    return extension.lower()


def get_file_format(filename: str) -> Type[SlicedModelFile]:
    logger.debug(f"Filename is {filename}")
    file_format = EXTENSION_TO_FILE_FORMAT.get(get_file_extension(filename))
    if file_format is CTBFile:
        file_format = check_encrypted(filename)
    assert file_format is not None
    return file_format


def get_supported_extensions() -> Set[str]:
    return set(EXTENSION_TO_FILE_FORMAT.keys())
