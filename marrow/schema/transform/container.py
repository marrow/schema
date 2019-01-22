from .base import Concern, Transform, Attribute


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
		
		value = (str(v) for v in value)
		
		if self.strip:
			value = (v.strip() for v in value)
		
		if not self.empty:
			value = (v for v in value if v)
		
		return value
	
	def native(self, value, context=None):
		"""Convert the given string into a list of substrings."""
		
		separator = self.separator.strip() if self.strip and hasattr(self.separator, 'strip') else self.separator
		value = super().native(value, context)
		
		if value is None:
			return self.cast()
		
		if hasattr(value, 'split'):
			value = value.split(separator)
		
		value = self._clean(value)
		
		try:
			return self.cast(value) if self.cast else value
		except Exception as e:
			raise Concern("{0} caught, failed to perform array transform: {1}", e.__class__.__name__, str(e))
	
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
			raise Concern("{0} caught, failed to convert to string: {1}", e.__class__.__name__, str(e))
		
		return super().foreign(value)


array = Array()
