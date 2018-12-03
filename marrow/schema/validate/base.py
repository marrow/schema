"""Marrow Schema base classes for data validation."""

from re import compile
from numbers import Number

from .. import Container, Attribute, CallbackAttribute
from ..exc import Concern
from ..util import ensure_tuple
from .util import SliceAttribute, RegexAttribute


# ## Class Definitions

class Validator(Container):
	"""Validate a value against one or more rules.
	
	Validators are generally run on Python-native datatypes, after, or before in the case of outgoing values, any
	transformations.
	
	Subclass and override the `validate` method to implement your own simple validators.
	"""
	
	def validate(self, value, context=None):
		"""Attempt to validate the given value.
		
		Return the value (possibly mutated in some way) or raise a Concern.  Reasons to alter during validation might
		be to localize the format of a phone number, or unicode normalize text.
		
		Context represents the current processing context, i.e. the object whose property is being inspected.
		"""
		return value


class Always(Validator):
	"""Always pass validation.
	
	Primarily useful to replace other validators for debugging purposes.  You can easily do this at import time:
	
		from marrow.schema.validation import Always as AlwaysRequired
	"""
	def validate(self, value=None, context=None):
		return value

always = Always()


class Never(Validator):
	"""Never pass validation.
	
	Primarily useful to replace other validators for debugging purposes.  See the Always docstring for details.
	"""
	def validate(self, value=None, context=None):
		raise Concern("Set to always fail.")

never = Never()


class AlwaysTruthy(Validator):
	"""A value must always be truthy."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if not bool(value):
			raise Concern("Value is missing or empty.")
		
		return value

truthy = AlwaysTruthy()


class Truthy(AlwaysTruthy):
	"""A more mixin-able version of AlwaysTruthy."""
	
	truthy = Attribute(default=False)
	
	def validate(self, value, context=None):
		from functools import partial
		instance = super().validate if self.truthy else partial(AlwaysTruthy.validate, self)
		return instance(value, context)


class AlwaysFalsy(Validator):
	"""A value must always be falsy."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if bool(value):
			raise Concern("Value should be falsy.")
		
		return value

falsy = AlwaysFalsy()


class Falsy(AlwaysFalsy):
	"""A more mixin-able version of AlwaysFalsy."""
	
	falsy = Attribute(default=False)
	
	def validate(self, value, context=None):
		instance = super(Falsy, self) if self.falsy else super(AlwaysFalsy, self)
		return instance.validate(value, context)


class AlwaysRequired(Validator):
	"""A value must always be provided."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if value is None:
			raise Concern("Value is required, but none was provided.")
		
		if hasattr(value, '__len__') and not len(value):
			raise Concern("Value is required, but provided value is empty.")
		
		return value

required = AlwaysRequired()


class Required(AlwaysRequired):
	"""A value may be required.  More mixin-able than AlwaysRequired."""
	
	required = Attribute(default=False)
	
	def validate(self, value, context=None):
		instance = super(Required, self) if self.required else super(AlwaysRequired, self)
		return instance.validate(value, context)


class AlwaysMissing(Validator):
	"""A value must not be provided."""

	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if value is not None and (not hasattr(value, '__len__') or len(value)):
			raise Concern("Value must be omitted, but value was provided.")
		
		return value

missing = AlwaysMissing()


class Missing(AlwaysMissing):
	"""A value must not be provided. More mixin-able than AlwaysMissing."""
	
	missing = Attribute(default=False)
	
	def validate(self, value, context=None):
		instance = super(Missing, self) if self.missing else super(AlwaysMissing, self)
		return instance.validate(value, context)


class Callback(Validator):
	"""Execute a simple callback to validate the value.
	
	The callback is called with the validator instance, value, and context.
	
	May simply return a Concern instance.
	
	For your daily dose of WTF-magic, you can use this validator as a decorator::
	
		@Callback
		def always(validator, value, context):
			return value
		
		assert isinstance(always, Callback)
		assert always.validate(27) == 27
	"""
	validator = Attribute(default=None)
	
	def validate(self, value=None, context=None):
		value = super().validate(value, context)
		
		if not self.validator:
			return value
		
		result = self.validator(self, value, context)
		
		if isinstance(result, Concern):
			raise result
		
		return result


class In(Validator):
	"""Value must be contained within the provided iterable.
	
	The choice selection may be a callback, however note that the callback is passed no arguments.
	
	The iterable may be either a collection of single values, or a collection of 2-tuples indicating value and label.
	"""
	
	choices = CallbackAttribute(default=None)
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		choices = self.choices
		
		if not choices:
			return value
		
		if (value, ) not in ensure_tuple(1, choices):
			raise Concern("Value is not in allowed list.")
		
		return value


class Contains(Validator):
	"""Value being validated must contain the given value."""
	
	contains = CallbackAttribute()
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		# Small dance to allow None as a valid comparison value.
		try:
			other = self.contains
		except AttributeError:
			return value
		
		if other not in value:
			raise Concern("Value does not contain: {0}", other)
		
		return value


class Length(Validator):
	"""Ensure the value has a length within the given range.
	
	The defined length may represent an integer maximum length or be a slice() instance to represent min/max/step.
	
	Non-empty can be defined as a Length(slice(1, None)).
	
	An exact lngth can be defined as Length(slice(size, size+1))
	"""
	
	length = SliceAttribute(default=None)
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if self.length is None:
			return value
		
		ln = len(value) if hasattr(value, '__len__') else None
		length = self.length
		
		if ln is None:
			raise Concern("Value can't be measured; must be between {0} and {1} long.", length.start, length.stop)
		
		elif ln not in range(*length.indices(ln + 1)):
			raise Concern("Length out of bounds; must be between {0} and {1} long.", length.start, length.stop)
		
		return value


class Range(Validator):
	"""Ensure the value is within a given range, inclusive."""
	
	minimum = CallbackAttribute(default=None)
	maximum = CallbackAttribute(default=None)
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if self.minimum is None and self.maximum is None:
			return value
		
		minimum = self.minimum
		maximum = self.maximum
		
		if minimum and maximum and not (minimum <= value <= maximum):
			raise Concern("Out of bounds; must be greater than {0} and less than {1}.",
					minimum, maximum)
		
		elif minimum and value < minimum:
			raise Concern("Too small; must be greater than {0}.", minimum)
		
		elif maximum and value > maximum:
			raise Concern("Too large; must be less than {1}.", maximum)
		
		return value


class Pattern(Validator):
	"""Match a regular expression."""
	
	pattern = RegexAttribute(default=None)
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if not self.pattern or value is None:
			return value
		
		if not self.pattern.match(value):
			raise Concern("Failed to match required pattern.")
		
		return value


class Instance(Validator):
	"""Ensure the value is an instance of the given class."""
	
	instance = Attribute(default=None)
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		if self.instance and not isinstance(value, self.instance):
			raise Concern("Value is not an instance of {0!r}.", self.instance)
		
		return value


class Subclass(Validator):
	"""Ensure the value is a subclass of the given class."""
	
	subclass = Attribute(default=None)
	
	def validate(self, value, context=None):
		value = super(Subclass, self).validate(value, context)
		
		if self.subclass and not issubclass(value, self.subclass):
			raise Concern("Value is not a subclass of {0!r}.", self.subclass)
		
		return value


class Equal(Validator):
	"""Ensure the value being validated equals another.
	
	The value to compare against may be a callback taking no arguments and returning the value for comparison.
	"""
	
	equals = CallbackAttribute()
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		# We perform this little dance to ensure None is a valid value.
		try:
			other = self.equals
		except AttributeError:
			return value
		
		if value != other:
			raise Concern("Value does not equal: {0}", other)
		
		return value


class Unique(Validator):
	"""Ensure the values of an iterable are unique.
	
	Works on built-in iterables such as lists, tuples, sets, etc. and even dictionaries, though it only checks
	dictionary values as the keys are already gaurenteed to be unique.  Must be able to transform into a set.
	"""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		_value = value.values() if hasattr(value, 'values') else value
		
		if not len(_value) == len(set(_value)):
			raise Concern("Not all values are unique.")
		
		return value

unique = Unique()


class Validated(Attribute):
	"""A small attribute helper to validate values as they are assigned.
	
	Primarily used as a mixin, i.e. to provide validation in addition to typecasting.
	"""
	
	validator = CallbackAttribute(default=always)
	
	def __set__(self, obj, value):
		"""Executed when assigning a value to a Validated instance attribute."""
		
		self.validator.validate(value, obj)
		
		# Store the (validated) value in the warehouse.
		super().__set__(obj, value)
