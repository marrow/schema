"""Marrow Schema metaclass definition.

This handles the irregularities of metaclass definition and usage across Python versions.
"""

from collections import OrderedDict as odict


class ElementMeta(type):
	"""Instantiation order tracking and attribute naming / collection metaclass.
	
	To use, construct subclasses of the Element class whose attributes are themselves instances of Element subclasses.
	Five attributes on your subclass have magical properties:
	
	* `inst.__sequence__`
	  An atomically incrementing (for the life of the process) counter used to preserve order.  Each instance of an
	  Element subclass is given a new sequence number automatically.
	  
	* `inst.__name__`
	  Element subclasses automatically associate attributes that are Element subclass instances with the name of the
	  attribute they were assigned to.
	  
	* `cls.__attributes__`
	  An ordered dictionary of all Element subclass instances assigned as attributes to your class. Class inheritance
	  of this attribute is handled differently: it is a combination of the `__attributes__` of all parent classes.
	  **Note:** This is only calculated at class construction time; this makes it efficient to consult frequently.
	  
	* `cls.__attributed__`
	  Called after class construction to allow you to easily perform additional work, post-annotation.
	  Should be a classmethod for full effect. Deprecatedi for many use cases; use Python's own `__init_subclass__`
	  instead. (This also allows arguments to be passed within the class definition, which is more flexible.)
	  
	* `cls.__fixup__`
	  If an instance of your Element subclass is assigned as a property to an Element subclass, this method of your
	  class will be called to notify you and allow you to make additional adjustments to the class using your subclass.
	  Should be a classmethod.
	
	Generally you will want to use one of the helper classes provided (Container, Attribute, etc.) however this can be
	useful if you only require extremely light-weight attribute features on custom objects.
	"""
	
	# Atomically incrementing sequence number.
	sequence = 0
	
	def __new__(meta, name, bases, attrs):
		"""Gather known attributes together, preserving order, and transfer attribute names to them."""
		
		# Short-circuit this logic on the root "Element" class, as it can have no attributes.
		if len(bases) == 1 and bases[0] is object:
			attrs['__attributes__'] = odict()
			return type.__new__(meta, str(name), bases, attrs)
		
		attributes = odict()
		overridden_sequence = dict()
		fixups = []
		
		# Gather the parent classes that participate in our protocol.
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
			"""Process attributes that are Element subclass instances."""
			
			# If no name has been defined, define it declaratively.
			if not getattr(attr, '__name__', None):
				attr.__name__ = name
			
			# If this attribute existed previously, clone the sequence number to preserve order.
			if name in overridden_sequence:
				attr.__sequence__ = overridden_sequence[name]
			
			# We give attributes a chance to perform additional work.
			if hasattr(attr, '__fixup__'):
				fixups.append(attr)  # Record the attribute to prevent __get__ transformation later.
			
			return name, attr
		
		# Iteratively process the Element subclass instances and update their definition.
		attributes.update(process(k, v) for k, v in attrs.items() if isinstance(v, Element))
		attrs['__attributes__'] = odict(sorted(attributes.items(), key=lambda t: t[1].__sequence__))
		
		# Construct the new class.
		cls = type.__new__(meta, str(name), bases, attrs)
		
		# Allow the class to be notified of its own construction.  Do not ask how this avoids creating black holes.
		if hasattr(cls, '__attributed__'):
			cls.__attributed__()
		
		# We do this now to allow mutation on the completed class.
		for obj in fixups:
			obj.__fixup__(cls)
		
		return cls
	
	def __call__(meta, *args, **kw):
		"""Automatically give each new instance an atomically incrementing sequence number."""
		
		instance = type.__call__(meta, *args, **kw)
		
		instance.__sequence__ = ElementMeta.sequence
		ElementMeta.sequence += 1
		
		return instance


Element = ElementMeta("Element", (object, ), dict())

class Element(metaclass=ElementMeta):
	pass
