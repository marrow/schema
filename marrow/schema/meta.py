# encoding: utf-8

"""Marrow Schema metaclass definition.

This handles the irregularities of metaclass definition and usage across Python versions.
"""

from .compat import odict


class ElementMeta(type):
	"""Instantiation order tracking and attribute naming / collection metaclass."""
	
	sequence = 0
	
	def __new__(meta, name, bases, attrs):
		"""Gather known attributes together, preserving order, and transfer attribute names to them."""
		
		if len(bases) == 1 and bases[0] is object:
			attrs['__attributes__'] = odict()
			return type.__new__(meta, name, bases, attrs)
		
		attributes = odict()
		overridden_sequence = dict()
		fixups = []
		
		for base in bases:
			if hasattr(base, '__attributes__'):
				attributes.update(base.__attributes__)
		
		# To allow for hardcoding of Attributes we eliminate keys that have been redefined.
		# They might get added back later, of course.
		for k in attrs:
			if k in attributes:
				overridden_sequence[k] = attributes[k].__sequence__
				attributes.pop(k, None)
		
		def process(name, attr):
			if not getattr(attr, '__name__', None):
				attr.__name__ = name
			
			if name in overridden_sequence:
				attr.__sequence__ = overridden_sequence[name]
			
			# We give attributes a chance to perform additional work.
			if hasattr(attr, '__fixup__'):
				fixups.append(attr)  # Record the attribute to prevent __get__ transformation later.
			
			return name, attr
		
		attributes.update(process(k, v) for k, v in attrs.items() if isinstance(v, Element))
		
		attrs['__attributes__'] = odict(sorted(attributes.items(), key=lambda t: t[1].__sequence__))
		
		result = type.__new__(meta, name, bases, attrs)
		
		if hasattr(result, '__attributed__'):
			result.__attributed__()
		
		for obj in fixups:
			obj.__fixup__(result)
		
		return result
	
	def __call__(meta, *args, **kw):
		"""Automatically give each new instance an atomically incrementing sequence number."""
		
		instance = type.__call__(meta, *args, **kw)
		
		instance.__sequence__ = ElementMeta.sequence
		ElementMeta.sequence += 1
		
		return instance


Element = ElementMeta("Element", (object, ), dict())
