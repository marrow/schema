# encoding: utf-8

"""Marrow Schema metaclass definition.

This handles the irregularities of metaclass definition and usage across Python versions.
"""

import sys

from collections import OrderedDict


class ElementMeta(type):
	"""Instantiation order tracking and attribute naming / collection metaclass."""
	
	sequence = 0
	
	def __new__(meta, name, bases, attrs):
		"""Gather known attributes together, preserving order, and transfer attribute names to them."""
		
		if len(bases) == 1 and bases[0] is object:
			attrs['__attributes__'] = OrderedDict()
			return type.__new__(meta, name, bases, attrs)
		
		attributes = OrderedDict()
		
		for base in bases:
			if hasattr(base, '__attributes__'):
				attributes.update(base.__attributes__)
		
		def process(name, attr):
			if not getattr(attr, '__name__', None):
				attr.__name__ = name
			return name, attr
		
		for k, v in sorted(
				(process(k, v) for k, v in attrs.items() if isinstance(v, Element)),
				key = lambda t: t[1].__sequence__):
			attributes[k] = v
		
		attrs['__attributes__'] = attributes
		
		return type.__new__(meta, name, bases, attrs)
	
	def __call__(meta, *args, **kw):
		"""Automatically give each new instance an atomically incrementing sequence number."""
		
		instance = type.__call__(meta, *args, **kw)
		
		instance.__sequence__ = ElementMeta.sequence
		ElementMeta.sequence += 1
		
		return instance


Element = ElementMeta("Element", (object, ), dict())
