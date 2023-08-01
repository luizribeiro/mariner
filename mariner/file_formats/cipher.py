from dataclasses import dataclass
import numpy as np
import hashlib

@dataclass
class Keyring86:
	initial: int
	key: int
	index: int

# Key encoding provided by:
# https://github.com/cbiffle/catibo/blob/master/doc/cbddlp-ctb.adoc
	@classmethod
	def __init__(self, seed: int, slicenum: int):
		initial = int(seed)*int(0x2d83cdac) + int(0xd8a83423)
		key = (int(slicenum*int(0x1e1530cd)) + int(0xec3d47cd)) * int(initial)
		self.initial = int(initial)
		self.key =  int(key)
		self.index = 0
	
	@classmethod
	def Next(self) -> bytes:
		k = int(self.key >> int((8 * self.index)))
		self.index += 1
		if self.index&3 == 0:
			self.key = int(self.key + self.initial)
			self.index = 0
		return k.to_bytes((k.bit_length() + 7) // 8, 'little')

	@classmethod
	def Read(self, data: bytes) -> bytes:
		out = bytearray()
		for i in data:
			temp = self.Next()
			out.extend([i^temp[0]])
		return bytes(out)
		
def cipher86(seed, slicenum, data):
	if seed == 0:
		return data
	else:
		kr = Keyring86(seed,slicenum)
		out = kr.Read(data)
		return out


@dataclass
class KeyringFDG:
	initial: int
	key: int
	index: int

# Key encoding provided by:
# https://github.com/cbiffle/catibo/blob/master/doc/cbddlp-ctb.adoc
	@classmethod
	def __init__(self, seed: int, slicenum: int):
		initial = int(seed)-int(0x1dcb76c3) ^ int(0x257e2431)
		key = int(initial*int(0x82391efd)) * int(slicenum ^ int(0x110bdacd))
		self.initial = int(initial)
		self.key =  int(key)
		self.index = 0
	
	@classmethod
	def Next(self) -> bytes:
		k = int(self.key >> int((8 * self.index)))
		self.index += 1
		if self.index&3 == 0:
			self.key = int(self.key + self.initial)
			self.index = 0
		return k.to_bytes((k.bit_length() + 7) // 8, 'little')


	@classmethod
	def Read(self, data: bytes) -> bytes:
		out = bytearray()
		for i in data:
			temp = self.Next()
			out.extend([i^temp[0]])
		return bytes(out)
		
def cipherFDG(seed, slicenum, data):
	if seed == 0:
		return data
	else:
		kr = KeyringFDG(seed,slicenum)
		out = kr.Read(data)
		return 
		
def computeSHA256Hash(input: bytes):
	output = hashlib.sha256()
	output.update(input)
	return output.digest()

# https://github.com/sn4k3/UVtools/blob/2625c13cc3179a55865e5594180050258ab60a95/UVtools.Core/Extensions/CryptExtensions.cs#L59
def xorCipher(text: bytes, key: bytes):
	output = bytearray(len(text))
	for i in range(len(text)):
		output[i] = (text[i] ^ key[i % len(key)])
	return output
