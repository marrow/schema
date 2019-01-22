import sys

from .. import Container, DataAttribute, Attribute, Attributes
from ..exc import Concern


class BaseTransform(Container):
	"""The core implementation of common Transform shared routines.
	
	Most transformer implementations should subclass Transform or SplitTransform.
	"""
	
	def foreign(self, value, context=None):
		"""Convert a value from Python to a foriegn-acceptable type, i.e. web-safe, JSON-safe, etc."""
		
		return value
	
	def native(self, value, context=None):
		"""Convert a value from a foreign type (i.e. web-safe) to Python-native."""
		
		return value
	
	def loads(self, value, context=None):
		"""Attempt to load a string-based value into the native representation.
		
		Empty strings are treated as ``None`` values.
		"""
		
		if value == '' or (hasattr(value, 'strip') and value.strip() == ''):
			return None
		
		return self.native(value)
	
	def dumps(self, value, context=None):
		"""Attempt to transform a native value into a string-based representation.
		
		``None`` values are represented as an empty string.
		"""
		
		if value is None:
			return ''
		
		return str(self.foreign(value))
	
	def load(self, fh, context=None):
		"""Attempt to transform a string-based value read from a file-like object into the native representation."""
		
		return self.loads(fh.read())
	
	def dump(self, fh, value, context=None):
		"""Attempt to transform and write a string-based foreign value to the given file-like object.
		
		Returns the length written.
		"""
		
		value = self.dumps(value)
		fh.write(value)
		return len(value)


class Transform(BaseTransform):
	"""The base transformer implementation.
	
	Like validation, may raise Concern on invalid input data.  The role of a transformer, though, is to expend
	Best Effort to transform values to and from a foreign format.  This base class defines two attributes:
	
	* ``encoding`` The encoding to use during any encoding/decoding that is required. (Default: ``utf-8``) 
	* ``strip`` Should string values be stripped of leading and trailing whitespace?  (Default: ``True``)
	
	Transformers should operate bi-directionally wherever possible.
	"""
	
	none = Attribute(default=False)  # Handle processing of empty string values into None values.
	encoding = Attribute(default='utf-8')  # Specify None to disable str-to-unicode conversion.
	strip = Attribute(default=True)  # Specify False to disable automatic text stripping.
	
	def native(self, value, context=None):
		"""Convert a value from a foriegn type (i.e. web-safe) to Python-native."""
		
		if self.strip and hasattr(value, 'strip'):
			value = value.strip()
		
		if self.none and value == '':
			return None
		
		if self.encoding and isinstance(value, bytes):
			return value.decode(self.encoding)
		
		return value


class IngressTransform(Transform):
	"""The simplest transformation, typecasting incoming data.
	
	Will attempt to use the ``ingress`` function to transform foreign values to native.  It is assumed that native
	values are acceptable as foreign values when using this transformer.  ``None`` is an acceptable value in all cases.
	
	(Combine this transformer with the Required validator if ``None`` values are not actually acceptable.)
	
	For example::
	
		integer = IngressTransform(ingress=int)
	
	Useful in conjunction with SplitTransform to produce simple custom (de)serializers.
	"""
	
	ingress = DataAttribute()
	
	def native(self, value, context=None):
		"""Convert a value from a foriegn type (i.e. web-safe) to Python-native."""
		
		value = super().native(value, context)
		
		if value is None: return
		
		try:
			return self.ingress(value)
		except Exception as e:
			raise Concern("Unable to transform incoming value: {0}", str(e))


class EgressTransform(Transform):
	"""As per IngressTransform, but for outgoing data."""
	
	egress = DataAttribute()
	
	def foreign(self, value, context=None):
		value = super().foreign(value, context)
		
		try:
			return self.egress(value)
		except Exception as e:
			raise Concern("Unable to transform outgoing value: {0}", str(e))


class CallbackTransform(IngressTransform, EgressTransform):
	"""A convienent combination of IngressTransform and EgressTransform.
	
	Both ``ingress`` and ``egress`` callbacks _must_ be supplied to function.
	"""
	pass


class SplitTransform(BaseTransform):
	"""Splits read and write behaviours between two transformers.
	
	Both ``reader`` and ``writer`` transformer instances are required to function.
	"""
	
	reader = DataAttribute()
	writer = DataAttribute()
	
	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)
		
		try:
			self.reader
			self.writer
		except AttributeError:
			raise Concern("SplitTransform instances must define both reader and writer child transformers.")
	
	# Reader Methods
	
	def native(self, value, context=None):
		return self.reader.native(value, context)
	
	def loads(self, value, context=None):
		return self.reader.loads(value, context)
	
	def load(self, fh, context=None):
		return self.reader.load(fh, context)
	
	# Writer Methods
	
	def foreign(self, value, context=None):
		return self.writer.foreign(value, context)
	
	def dumps(self, value, context=None):
		return self.writer.dumps(value, context)
	
	def dump(self, fh, value, context=None):
		return self.writer.dump(fh, value, context)
