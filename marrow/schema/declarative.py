"""Marrow Schema base class definitions.

These are the most frequently used base classes provided by Marrow Schema.
"""

from warnings import warn
from inspect import isroutine
from collections import OrderedDict as odict, deque
from collections.abc import MutableMapping
from .meta import Element


class Container(Element):
	"""The underlying machinery for handling class instantiation for schema elements whose primary purpose is
	containing other schema elements, i.e. Document, Record, CompoundWidget, etc.
	
	Association of declarative attribute names (at class construction time) is handled by the Element metaclass.
	
	Container subclasses have one additional magical property:
	
	* ``inst.__data__``
	  Primary instance data storage for all DataAttribute subclass instances.  Equivalent to ``_data`` from MongoEngine.
	"""
	
	__store__ = dict  # The callable used to produce a new self.__data__ instance. Should result in a MutableMapping.
	
	def __init__(self, *args, **kw):
		"""Process arguments and assign values to instance attributes at class instantiation time.
		
		Basically defining ``__init__`` so you don't have to.
		
		You can extend this to support validation during instantiation, or to process additional programmatic
		arguments.
		"""
		
		# Inherit behaviour from Element, notably we want to track our instantiation sequence.
		super().__init__()
		
		# Do the heavy lifting of merging positional and keyword arguments.
		arguments = self._process_arguments(args, kw)
		
		# Prepare the attribute value warehouse for this instance.
		self.__data__ = self.__store__()
		
		assert isinstance(self.__data__, MutableMapping), "Data storage attribute __data__ must be a mutable mapping."
		
		# Assign valid attributes.
		for name, value in arguments.items():
			setattr(self, name, value)
	
	def _process_arguments(self, args, kw):
		"""Map positional to keyword arguments, identify invalid assignments, and return the result.
		
		This is likely generic enough to be useful as a standalone utility function, and goes to a fair amount of
		effort to ensure raised exceptions are as Python-like as possible.
		"""
		
		# Ensure we were not passed too many arguments.
		if len(args) > len(self.__attributes__):
			raise TypeError('{0} takes no more than {1} argument{2} ({3} given)'.format(
					self.__class__.__name__,
					len(self.__attributes__),
					'' if len(self.__attributes__) == 1 else 's',
					len(args)
				))
		
		# Retrieve the names associated with the positional parameters.
		names = [name for name in self.__attributes__.keys() if name[0] != '_' or name == '__name__'][:len(args)]
		
		# Sets provide a convienent way to identify intersections.
		duplicates = set(kw.keys()) & set(names)
		
		# Given duplicate values, explode gloriously.
		if duplicates:
			raise TypeError('{0} got multiple values for keyword argument{1}: {2}'.format(
					self.__class__.__name__,
					'' if len(duplicates) == 1 else 's',
					', '.join(duplicates)
				))
		
		def field_values(args, kw):
			"""A little closure to yield out fields and their assigned values in field order."""
			
			for i, arg in enumerate(self.__attributes__.keys()):
				if len(args):
					yield arg, args.popleft()
				
				if arg in kw:
					yield arg, kw.pop(arg)
		
		result = odict(field_values(deque(args), dict(kw)))
		
		# Again use sets, this time to identify unknown keys.
		unknown = set(kw.keys()) - set(result.keys())
		
		# Given unknown keys, explode gloriously.
		if unknown:
			raise TypeError('{0} got unexpected keyword argument{1}: {2}'.format(
					self.__class__.__name__,
					'' if len(unknown) == 1 else 's',
					', '.join(unknown)
				))
		
		return result


class DataAttribute(Element):
	"""Descriptor protocol support for Element subclasses.
	
	The base attribute class which implements the descriptor protocol, pulling the instance value of the attribute from
	the containing object's ``__data__`` dictionary.  If an attempt is made to read an attribute that does not have a
	corresponding value in the data dictionary an ``AttributeError`` will be raised.
	"""
	
	def __get__(self, obj, cls=None):
		"""Executed when retrieving a DataAttribute instance attribute."""
		
		# If this is class attribute (and not instance attribute) access, we return ourselves.
		if obj is None:
			return self
		
		# Attempt to retrieve and return the data from the warehouse.
		try:
			return obj.__data__[self.__name__]
		except KeyError:
			raise AttributeError('\'{0}\' object has no attribute \'{1}\''.format(
					obj.__class__.__name__,
					self.__name__
				))
	
	def __set__(self, obj, value):
		"""Executed when assigning a value to a DataAttribute instance attribute."""
		
		# Simply store the value in the warehouse.
		obj.__data__[self.__name__] = value
	
	def __delete__(self, obj):
		"""Executed via the ``del`` statement with a DataAttribute instance attribute as the argument."""
		
		# Delete the data completely from the warehouse.
		del obj.__data__[self.__name__]


class Attribute(Container, DataAttribute):
	"""Re-naming, default value, and container support for data attributes.
	
	All "data" is stored in the container's ``__data__`` dictionary.  The key defaults to the Attribute's instance name
	and can be overridden, unlike DataAttribute, by passing a name as the first positional parameter, or as the
	``name`` keyword argument.
	
	May contain nested Element instances to define properties for your Attribute subclass declaratively.
	
	If ``assign`` is True and the default value is ever utilized, immediately pretend the default value was assigned to
	this attribute.  (Override this in subclasses.)
	"""
	
	__name__ = DataAttribute()
	default = DataAttribute()
	assign = False  # If the value is missing, do we outright create it?
	
	def __init__(self, *args, **kw):
		"""A tiny helper to work around the dunderscores around ``name`` during instantiation.
		
		The value must always be retrieved as ``inst.__name__``, but may be assigned using the shorthand.
		"""
		
		# Re-map ``name`` to ``__name__`` in the keyword arguments, if present.
		if 'name' in kw:
			kw['__name__'] = kw.pop('name')
		
		# Process arguments upstream.
		super().__init__(*args, **kw)
	
	def __get__(self, obj, cls=None):
		"""Executed when retrieving an Attribute instance attribute."""
		
		# If this is class attribute (and not instance attribute) access, we return ourselves.
		if obj is None:
			return self
		
		# Attempt to retrieve the data from the warehouse.
		try:
			return super().__get__(obj, cls)
		except AttributeError:
			pass
		
		# Attempt to utilize the defined default value.
		try:
			default = self.default
		except AttributeError:
			pass
		else:
			# Process and optionally store the default value.
			value = default() if isroutine(default) else default
			if self.assign:
				self.__set__(obj, value)
			return value
		
		# If we still don't have a value, this attribute doesn't yet exist.
		raise AttributeError('\'{0}\' object has no attribute \'{1}\''.format(
				obj.__class__.__name__,
				self.__name__
			))


class CallbackAttribute(Attribute):
	"""An attribute that automatically executes the value upon retrieval, if a callable routine.
	
	Frequently used by validation, transformation, and object mapper systems.
	"""
	
	def __get__(self, obj, cls=None):
		"""Executed when retrieving an Attribute instance attribute."""
		
		# If this is class attribute (and not instance attribute) access, we return ourselves.
		if obj is None:
			return self
		
		# Attempt to retrieve the data from the warehouse.
		value = super().__get__(obj, cls)
		
		# Return the value, or execute it and return the result.
		return value() if isroutine(value) else value


# ## Deprecated Classes
# Deprecated naming conventions; for legacy use only.

class BaseAttribute(Container):
	"""BaseAttribute is now called Container."""
	
	def __init__(self, *args, **kw):
		warn("Use of BaseAttribute is deprecated, use Container instead.", DeprecationWarning)
		super().__init__(*args, **kw)


class BaseDataAttribute(Container):
	"""BaseDataAttribute is now called DataAttribute."""
	
	def __init__(self, *args, **kw):
		warn("Use of BaseDataAttribute is deprecated, use DataAttribute instead.", DeprecationWarning)
		super().__init__(*args, **kw)
