# encoding: utf-8

from .compat import odict
from .declarative import Container, Attribute


class Attributes(Container):
	"""Easily access the known declarative attributes of an object, preserving definition order."""
	
	only = Attribute(default=None)  # Filter results based to instances of these.
	
	def __get__(self, obj, cls=None):
		# make this into a view on top of obj.__attributes__
		if not obj:
			obj = cls
		
		if not self.only:
			return obj.__attributes__.copy()
		
		return odict((k, v) for k, v in obj.__attributes__.items() if isinstance(v, self.only))


def ensure_tuple(length, tuples):
	"""Yield `length`-sized tuples from the given collection.
	
	Will truncate longer tuples to the desired length, and pad using the leading element if shorter.
	"""
	for elem in tuples:
		if not isinstance(elem, (tuple, list)):
			yield (elem, ) * length
			continue
		
		l = len(elem)
		
		if l == length:
			yield elem
		
		elif l > length:
			yield tuple(elem[:length])
		
		elif l < length:
			yield (elem[0], ) * (length - l) + tuple(elem)


# Deprecated naming conventions; for legacy use only.

DeclarativeAttributes = Attributes
