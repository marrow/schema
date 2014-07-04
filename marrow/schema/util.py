# encoding: utf-8

try:  # pragma: no cover
	from collections import OrderedDict
except ImportError:  # pragma: no cover
	from ordereddict import OrderedDict

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
		
		return OrderedDict((k, v) for k, v in obj.__attributes__.items() if isinstance(v, self.only))


# Deprecated naming conventions; for legacy use only.

DeclarativeAttributes = Attributes
