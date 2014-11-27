# encoding: utf-8

from __future__ import unicode_literals

from ..compat import unicode
from .base import Concern, Transform, Attribute


class Boolean(Transform):
	"""Convert boolean values.
	
	Intelligently handles boolean and non-string values, returning as-is and passing to the bool builtin resspectively.
	
	This process is case-insensitive.  Acceptable values:
	
	Truthy:
	
	* true
	* t
	* yes
	* y
	* on
	* 1
	
	Falsy:
	
	* false
	* f
	* no
	* n
	* off
	* 0
	
	These default lists can be overridden with the ``truthy`` and ``falsy`` attributes.  When converting native values
	to foreign ones, the first value in the truthy/falsy lists is used based on the truthiness of the value; if you
	wish to restrict to only actual boolean values combine this with a validator.
	"""
	
	none = Attribute(default=True)
	truthy = Attribute(default=('true', 't', 'yes', 'y', 'on', '1'))
	falsy = Attribute(default=('false', 'f', 'no', 'n', 'off', '0'))
	
	def native(self, value, context=None):
		"""Convert a foreign value to a native boolean."""
		
		value = super(Boolean, self).native(value, context)
		
		if self.none and (value is None):
			return None
		
		try:
			value = value.lower()
		except AttributeError:
			return bool(value)
		
		if value in self.truthy:
			return True
		
		if value in self.falsy:
			return False
		
		raise Concern("Unable to convert {0!r} to a boolean value.", value)
	
	def foreign(self, value, context=None):
		"""Convert a native value to a textual boolean."""
		
		if self.none and value is None:
			return ''
		
		try:
			value = self.native(value, context)
		except Concern:
			# The value might not be in the lists; bool() evaluate it instead.
			value = bool(value.strip() if self.strip and hasattr(value, 'strip') else value)
		
		if value in self.truthy or value:
			return self.truthy[0]
		
		return self.falsy[0]

boolean = Boolean()


class Array(Transform):
	"""Convert array-like values.
	
	Intelligently handles list and non-string values, returning as-is and passing to the list builtin respectively.
	
	For a more advanced method of converting between strings and iterables see the Token transformer.
	
	With the provided defaults (comma separator, exclusion of empty elements, stripping of whitespace, and casting to
	a list) the following example applies::
	
		"foo,bar, baz   , , diz" -> ['foo', 'bar', 'baz', 'diz'] -> "foo,bar,baz,diz"
	"""
	
	separator = Attribute(default=', ')
	empty = Attribute(default=False)  # allow elements that appear 'empty' to be included
	cast = Attribute(default=list)  # return native results as an instance of this, None for a lazy generator
	
	def _clean(self, value):
		"""Perform a standardized pipline of operations across an iterable."""
		
		value = (unicode(v) for v in value)
		
		if self.strip:
			value = (v.strip() for v in value)
		
		if not self.empty:
			value = (v for v in value if v)
		
		return value
	
	def native(self, value, context=None):
		"""Convert the given string into a list of substrings."""
		
		separator = self.separator.strip() if self.strip and hasattr(self.separator, 'strip') else self.separator
		value = super(Array, self).native(value, context)
		
		if value is None:
			return self.cast()
		
		if hasattr(value, 'split'):
			value = value.split(separator)
		
		value = self._clean(value)
		
		try:
			return self.cast(value) if self.cast else value
		except Exception as e:
			raise Concern("{0} caught, failed to perform array transform: {1}", e.__class__.__name__, unicode(e))
	
	def foreign(self, value, context=None):
		"""Construct a string-like representation for an iterable of string-like objects."""
		
		if self.separator is None:
			separator = ' '
		else:
			separator = self.separator.strip() if self.strip and hasattr(self.separator, 'strip') else self.separator
		
		value = self._clean(value)
		
		try:
			value = separator.join(value)
		except Exception as e:
			raise Concern("{0} caught, failed to convert to string: {1}", e.__class__.__name__, unicode(e))
		
		return super(Array, self).foreign(value)

array = Array()


class Number(Transform):
	pass


class Token(Transform):
	pass



# VETO: Extract

'''
class DateTimeTransform(Transform):
	base = Attribute(defualt=datetime.datetime)
	format = "%Y-%m-%d %H:%M:%S"
	
	def __call__(self, value):
		if not value:
			return ''
		
		return super(DateTimeTransform, self)(value.strftime(self.format))
	
	def native(self, value):
		value = super(DateTimeTransform, self).native(value)
		
		return self.base.strptime(value, self.format)
'''
