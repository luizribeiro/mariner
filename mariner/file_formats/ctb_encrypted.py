import pathlib
import struct
from dataclasses import dataclass
from typing import List
import numpy as np

import png
from typedstruct import LittleEndianStruct, StructType

from mariner.file_formats import SlicedModelFile
from mariner.file_formats.cipher import xorCipher, computeSHA256Hash

import base64
from Crypto.Cipher import AES

from mariner.file_formats.ctb import CTBFile

MAGIC_CTB_ENCRYPTED = 0x12FD0107
HASH_LENGTH = 32
BHASH = b'32'

about_software = "UVtools"
secret1 = "hQ36XB6yTk+zO02ysyiowt8yC1buK+nbLWyfY40EXoU="
secret2 = "Wld+ampndVJecmVjYH5cWQ=="
bigfoot = xorCipher(base64.b64decode(secret1, validate=True), about_software.encode())
cookiemonster = xorCipher(base64.b64decode(secret2, validate=True), about_software.encode())

@dataclass(frozen=True)
class CTBEncryptedHeader(LittleEndianStruct):
    magic: int = StructType.uint32()
    slicer_size: int = StructType.uint32()
    slicer_offset: int =  StructType.uint32()
    unknown_01: int =  StructType.uint32()
    unknown_02: int =  StructType.uint32()
    signature_size: int =  StructType.uint32()
    signature_offset: int = StructType.uint32()
    unknown_03: int =  StructType.uint32()
    unknown_04: int = StructType.uint16()
    unknown_05: int = StructType.uint16()
    unknown_06: int = StructType.uint32()
    unknown_07: int =  StructType.uint32()
    unknown_08: int =  StructType.uint32()

@dataclass(frozen=True)
class CTBEncryptedSlicer(LittleEndianStruct):
    checksum_value: int = StructType.uint64()
    layer_table_offset: int = StructType.uint32()
    display_width: float = StructType.float32()
    display_height: float = StructType.float32()
    machine_z: float = StructType.float32()
    unknown_01: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    total_height_mm: float = StructType.float32()
    layer_height_mm: float = StructType.float32()
    exposure_time: float = StructType.float32()
    bottom_exposure_time: float = StructType.float32()
    light_off_delay: float = StructType.float32()
    bottom_layer_count: int = StructType.uint32()
    resolution_x: int = StructType.uint32()
    resolution_y: int = StructType.uint32()
    layer_count: int = StructType.uint32()
    large_preview_offset: int = StructType.uint32()
    small_preview_offset: int = StructType.uint32()
    print_time: int = StructType.uint32()
    projector_type: int = StructType.uint32()
    bottom_lift_height: float = StructType.float32()
    bottom_lift_speed: float = StructType.float32()
    lift_height: float = StructType.float32()
    lift_speed: float = StructType.float32()
    retract_speed: float = StructType.float32()
    material_mm: float = StructType.float32()
    material_grams: float = StructType.float32()
    material_cost: float = StructType.float32()
    bottom_light_off_delay: float = StructType.float32()
    unknown_03: int = StructType.uint32()
    light_pwm: int = StructType.uint16()
    bottom_light_pwm: int = StructType.uint16()
    layer_xor_key: int = StructType.uint32()
    bottom_lift_height2: float = StructType.float32()
    bottom_lift_speed2: float = StructType.float32()
    lift_height2: float = StructType.float32()
    lift_speed2: float = StructType.float32()
    retract_height2: float = StructType.float32()
    retract_speed2: float = StructType.float32()
    rest_time_after_lift: float = StructType.float32()
    machine_name_offset: int = StructType.uint32()
    machine_name_size: int = StructType.uint32()
    per_layer_settings: int = StructType.uint32()
    unknown_04: int = StructType.uint32()
    unknown_05: int = StructType.uint32()
    rest_time_after_retract: float = StructType.float32()
    rest_time_after_lift2: float = StructType.float32()
    transition_layer_count: int = StructType.uint32()
    bottom_retract_speed: float = StructType.float32()
    bottom_retract_speed2: float = StructType.float32()
    padding1: int = StructType.uint32()
    four1: float = StructType.float32()
    padding2: int = StructType.uint32()
    four2: float = StructType.float32()
    rest_time_after_retract2: float = StructType.float32()
    rest_time_after_lift3: float = StructType.float32()
    rest_time_before_lift: float = StructType.float32()
    bottom_retract_height2: float = StructType.float32()
    unknown_06: int = StructType.uint32()
    unknown_07: int = StructType.uint32()
    unknown_08: int = StructType.uint32()
    last_layer_index: int = StructType.uint32()
    padding3: int = StructType.uint32()
    padding4: int = StructType.uint32()
    padding5: int = StructType.uint32()
    padding6: int = StructType.uint32()
    disclaimer_offset: int = StructType.uint32()
    disclaimer_size: int = StructType.uint32()
    padding7: int = StructType.uint32()
    padding8: int = StructType.uint32()
    padding9: int = StructType.uint32()
    padding10: int = StructType.uint32()
    #machine_name: bytes = StructType.chars()

@dataclass(frozen=True)
class CTBLayerPointer(LittleEndianStruct):
    layer_offset: int = StructType.uint32()
    padding_01: int = StructType.uint32()
    layer_table_size: int = StructType.uint32()
    padding_02: int = StructType.uint32()
    

@dataclass(frozen=True)
class CTBEncryptedLayerDef(LittleEndianStruct):
    table_size: int = StructType.uint32()
    position_z: float = StructType.float32()
    exposure_time: float = StructType.float32()
    light_off_delay: float = StructType.float32()
    layer_def_offset: int = StructType.uint32()
    unknown_02: int = StructType.uint32()
    data_length: int = StructType.uint32()
    unknown_03: int = StructType.uint32()
    encrypted_data_offset: int = StructType.uint32()
    encrypted_data_length: int = StructType.uint32()
    lift_height: float = StructType.float32()
    lift_speed: float = StructType.float32()
    lift_height2: float = StructType.float32()
    lift_speed2: float = StructType.float32()
    retract_speed: float = StructType.float32()
    retract_height2: float = StructType.float32()
    retract_speed2: float = StructType.float32()
    rest_time_before_lift: float = StructType.float32()
    rest_time_after_lift: float = StructType.float32()
    rest_time_after_retract: float = StructType.float32()
    light_pwm: float = StructType.float32()
    unknown_06: int = StructType.uint32()

@dataclass(frozen=True)
class CTBPreview(LittleEndianStruct):
    resolution_x: int = StructType.uint32()
    resolution_y: int = StructType.uint32()
    image_offset: int = StructType.uint32()
    image_length: int = StructType.uint32()


REPEAT_RGB15_MASK: int = 1 << 5

def check_encrypted(filename: str):
    with open(filename, "rb") as file:
            ctb_header = CTBEncryptedHeader.unpack(file.read(CTBEncryptedHeader.get_size()))
            if ctb_header.magic == MAGIC_CTB_ENCRYPTED:
                return CTBEncryptedFile
            else:
                return CTBFile

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
    
def _aes_crypt(enc: bytes, encrypt: bool):
    Cipher = AES.new(bytes(bigfoot), AES.MODE_CBC, bytes(cookiemonster))

    temp = bytearray()
    temp += enc
    if len(enc) % 16 != 0:
        temp += ((16 - len(enc) % 16)* 'X')

    if encrypt:
        return Cipher.encrypt(bytes(temp))
    else:
        return Cipher.decrypt(bytes(temp))

@dataclass(frozen=True)
class CTBEncryptedFile(SlicedModelFile):
    @classmethod
    def read(self, path: pathlib.Path) -> "CTBEncryptedFile":
        with open(str(path), "rb") as file:
            ctb_header = CTBEncryptedHeader.unpack(file.read(CTBEncryptedHeader.get_size()))
            if ctb_header.magic != MAGIC_CTB_ENCRYPTED:
                raise TypeError("Not a valid encrypted CTB file\n" + str(ctb_header.magic) + "\n" + str(MAGIC_CTB_ENCRYPTED))

            file.seek(ctb_header.slicer_offset)
            encrypted_block = file.read(ctb_header.slicer_size)
            
            decrypted_block = _aes_crypt(encrypted_block, False)
            try:
                ctb_slicer = CTBEncryptedSlicer.unpack(decrypted_block)
            except:
                raise Exception("len(decrypted_block) = " + str(len(decrypted_block)))

            file.seek(ctb_slicer.machine_name_offset)
            printer_name = file.read(ctb_slicer.machine_name_size).decode()

            # Validate hash
            checksum_bytes = ctb_slicer.checksum_value.to_bytes(8, 'little')
            checksum_hash = computeSHA256Hash(checksum_bytes)
            encrypted_hash = _aes_crypt(checksum_hash, True)

            file.seek(-HASH_LENGTH, 2)
            hash = file.read(HASH_LENGTH)
            if not (set(hash) == set(encrypted_hash)):
                raise TypeError("The file checksum does not match, malformed file.\n" + str(hash) + "\n" + str(encrypted_hash) + "\n" + str(int.from_bytes(hash, 'little')) + "\n" + str(int.from_bytes(encrypted_hash, 'little')) + "\n" + str(int.from_bytes(checksum_hash, 'little')))

            LayersPointer = [None] * ctb_slicer.layer_count
            for layer_index in range(0, ctb_slicer.layer_count):
                file.seek(ctb_slicer.layer_table_offset)
                LayersPointer[layer_index] = CTBLayerPointer.unpack(file.read(CTBLayerPointer.get_size()))

            LayersDefinition = [None] * ctb_slicer.layer_count
            buggy_layers = []
            end_byte_offset_by_layer = []
            for layer in range(0, ctb_slicer.layer_count):
                file.seek(LayersPointer[layer].layer_offset)
                LayersDefinition[layer] = CTBEncryptedLayerDef.unpack(file.read(CTBEncryptedLayerDef.get_size()))
                end_byte_offset_by_layer.append(
                    LayersDefinition[layer].encrypted_data_offset + LayersDefinition[layer].encrypted_data_length
                )
    
            return CTBEncryptedFile(
                filename=path.name,
                bed_size_mm=(
                    round(ctb_slicer.display_width, 4),
                    round(ctb_slicer.display_height, 4),
                    round(ctb_slicer.machine_z, 4),
                ),
                height_mm=ctb_slicer.total_height_mm,
                layer_height_mm=ctb_slicer.layer_height_mm,
                layer_count=ctb_slicer.layer_count,
                resolution=(ctb_slicer.resolution_x, ctb_slicer.resolution_y),
                print_time_secs=ctb_slicer.print_time,
                end_byte_offset_by_layer=end_byte_offset_by_layer,
                # Unable to find these in new slicer format
                slicer_version=".".join(
                    [
                        str(1),
                        str(1),
                        str(9),
                        str(1),
                    ]
                ),
                printer_name=printer_name,
            )

    @classmethod
    def read_preview(cls, path: pathlib.Path) -> png.Image:
        with open(str(path), "rb") as file:
            ctb_header = CTBEncryptedHeader.unpack(file.read(CTBEncryptedHeader.get_size()))
            file.seek(ctb_header.slicer_offset)
			# We have to decrypt the block to get the preview information
            encrypted_block = file.read(CTBEncryptedSlicer.get_size())
            decrypted_block = _aes_crypt(encrypted_block, False)
            ctb_slicer = CTBEncryptedSlicer.unpack(decrypted_block)
            file.seek(ctb_slicer.large_preview_offset)
            preview = CTBPreview.unpack(file.read(CTBPreview.get_size()))

            file.seek(preview.image_offset)
            data = file.read(preview.image_length)

            return _read_image(preview.resolution_x, preview.resolution_y, data)
