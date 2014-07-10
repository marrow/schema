# encoding: utf-8

from __future__ import unicode_literals

import sys

from .. import Container, Attribute, Attributes


if sys.version_info > (3, ):
	unicode = str
	str = bytes


class TransformException(Exception):
	pass


class Transform(Container):
	encoding = Attribute(default='utf-8')
	
	def __call__(self, value):
		"""Convert a value from Python to a foriegn-acceptable type, i.e. web-safe."""
		
		if value is None:
			return ''
		
		return unicode(value, self.encoding)
	
	def native(self, value):
		"""Convert a value from a foriegn type (i.e. web-safe) to Python-native."""
		
		value = value.strip()
		
		if not value:
			return None
		
		if isinstance(value, str):
			return value.decode(self.encoding)
		
		return value


class SimpleTransform(Transform):
	pass


class ChainTransform(Transform):
	pass
