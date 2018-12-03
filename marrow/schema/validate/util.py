from re import compile
from numbers import Number

from .. import CallbackAttribute


class SliceAttribute(CallbackAttribute):
	"""Automatically consume iterables to ensure the assigned value is always a slice() instance."""
	
	@staticmethod
	def __cast(value):
		if isinstance(value, Number):
			value = (value, )
		
		if not isinstance(value, slice):
			value = slice(*value)
		
		return value
	
	def __wrap(self, fn):
		def inner():
			return self.__cast(fn())
		
		return inner
	
	def __set__(self, obj, value):
		if callable(value):
			return super().__set__(obj, self.__wrap(value))
		
		return super().__set__(obj, self.__cast(value))


class RegexAttribute(CallbackAttribute):
	"""Automatically attempt to transform non-regexen into regexen upon assignment.
	
	Technically only checks for regex-like capability a la a `.match()` method.  Will compile strings into regex objects.
	"""
	
	def __set__(self, obj, value):
		if not hasattr(value, 'match'):
			value = compile(value)
		
		return super().__set__(obj, value)
