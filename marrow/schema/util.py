"""Convienent utilities."""

from collections import OrderedDict as odict
from warnings import warn
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
		# Handle non-tuples and non-lists as a single repeated element.
		if not isinstance(elem, (tuple, list)):
			yield (elem, ) * length
			continue
		
		l = len(elem)
		
		# If we have the correct length already, yield it.
		if l == length:
			yield elem
		
		# If we're too long, truncate.
		elif l > length:
			yield tuple(elem[:length])
		
		# If we're too short, pad the *leading* element out.
		elif l < length:
			yield (elem[0], ) * (length - l) + tuple(elem)


class DeclarativeAttributes(Attributes):
	"""DeclarativeAttributes is now called Attributes."""
	
	def __init__(self, *args, **kw):
		warn("Use of DeclarativeAttributes is deprecated, use Attributes instead.", DeprecationWarning)
		super().__init__(*args, **kw)
