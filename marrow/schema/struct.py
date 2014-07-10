# encoding: utf-8

"""An example declarative schema for packed structures."""

from __future__ import absolute_import, unicode_literals

import sys
import struct

from .meta import ElementMeta
from .declarative import Container, DataAttribute, Attribute


# Byte order, size, and alignment markers.

NATIVE = b'@'
PORTABLE = b'='
LITTLE_ENDIAN = b'<'
BIG_ENDIAN = b'>'
NETWORK = b'!'



# Custom metaclass derivative to implement some class-level nicities.

class StructMeta(ElementMeta):
	def __len__(cls):
		"""Calculate the length, in bytes, of the structure.
		
		If the number of bytes is unbounded (i.e. by involving cstrings or pstrings), ValueError will be raised.
		"""
		return struct.calcsize(''.join(cls.__format__))
	
	@property
	def __format__(cls):
		





# Core classes.

class Struct(Container):
	"""A collection of individual fields."""
	
	__marker__ = NETWORK
	
	# Serialization / Deserialization Methods
	
	def dump(self, fh, offset=0):
		pass

	def dumps(self):
		pass

	@classmethod
	def load(self, fh, offset=0):
		pass

	@classmethod
	def loads(self, str):
		pass
	
	# Python Magic Methods
	
	def __bytes__(self):
		pass
	
	if sys.version_info < (3, ):
		__str__ = __bytes__
	
	def __len__(self):
		pass
	
	def __iter__(self):
		"""Iterate through the encoded field values.
		
		This is potentially useful for streaming encoded data, and repeatedly calls dumps() on the nested structures.
		
		Used internally to implement dump()/dumps().
		"""
		pass
	
	# Magic Declarative Methods
	
	def __attributed__(self):
		pass
	
	def __fixup__(self, instance):
		if isinstance(instance, Struct):
			self._child = True
		else:
			self._child = False
	
	# Magic Struct Schema Methods
	
	@classmethod
	def __format__(self):
		if not self._child:
			yield self.__marker__
		
		current = None
		
		return cls.__marker__ + ''.join(i.__format__ for i in self.__attributes__.values())


class Field(Attribute):
	"""Inherits "default" """
	_format = b''
	
	def __len__(self):
		return struct.calcsize(self.__format__)
	
	@property
	def __format__(self):
		return self._format
