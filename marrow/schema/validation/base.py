# encoding: utf-8

from __future__ import unicode_literals

import sys
import copy

from .. import Container, Attribute, Attributes
from ..compat import unicode
from ..util import ensure_tuple
from .exc import Concern


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
	
	Primarily useful to replace other validators for debugging purposes.  You can easily do this at import time::
	
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
		value = super(Required, self).validate(value, context)
		
		if not bool(value):
			raise Concern("Value is missing or empty.")
		
		return value

truthy = AlwaysTruthy()


class Truthy(AlwaysTruthy):
	"""A more mixin-able version of AlwaysTruthy."""
	
	truthy = Attribute(default=False)
	
	def validate(self, value, context=None):
		from functools import partial
		instance = super(Truthy, self).validate if self.truthy else partial(AlwaysTruthy.validate, self)
		return instance(value, context)


class AlwaysFalsy(Validator):
	"""A value must always be truthy."""
	
	def validate(self, value, context=None):
		value = super(AlwaysFalsy, self).validate(value, context)
		
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
		value = super(Required, self).validate(value, context)
		
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
		value = super(AlwaysMissing, self).validate(value, context)
		
		if value is not None or (hasattr(value, '__len__') and len(value)):
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
	
	The callback is called with the validator instance, value, and context.  May return True, a 2-tuple of
	`(level, message)` to signal failure, or any other value which is then ignored.
	
	For your daily dose of WTF-magic, you can use this validator as a decorator::
	
		@Callback
		def always(validator, value, context):
			return True
		
		assert isinstance(always, Callback)
		assert always.validate() ==
	"""
	validator = Attribute(default=None)
	
	def validate(self, value=None, context=None):
		if super(Callback, self).validate(value, context):
			return True
		
		if not self.validator:
			return
		
		result = self.validator(self, value, context)
		
		if isinstance(result, Concern):
			raise result
		elif result is not True and result:
			raise Concern(*result)
		
		return result


class In(Validator):
	"""Value must be contained within the provided iterable.
	
	The choice selection may be a callback, however note that the callback is passed no arguments.
	
	The iterable may be either a collection of single values, or a collection of 2-tuples indicating value and label.
	"""
	
	choices = Attribute(default=None)
	
	def validate(self, value, context=None):
		if super(In, self).validate(value, context):
			return True
		
		if not self.choices:
			return
		
		choices = self.choices() if callable(self.choices) else self.choices
		
		if (value, ) not in ensure_tuple(1, choices):
			raise Concern(ERROR, "Value is not in allowed list.")


class Contains(Validator):
	"""Value being validated must contain the given value."""
	
	contains = Attribute()
	
	def validate(self, value, context=None):
		if super(Contains, self).validate(value, context):
			return True
		
		# Small dance to allow None as a valid comparison value.
		try:
			other = self.contains() if callable(self.contains) else self.contains
		except AttributeError:
			return
		
		if other not in value:
			raise Concern(ERROR, "Value does not contain: {0}", other)


class Length(Validator):
	"""Ensure the value has a length within the given range.
	
	The defined length may represent an integer maximum length or be a slice() instance to represent min/max/step.
	
	Non-empty can be defined as a Length(slice(1,None))
	"""
	
	length = Attribute(default=None)  # TODO: Ensure this is a slice().  Tuples turn into slice(*value)
	
	def validate(self, value, context=None):
		if super(LengthValidator, self).validate(value, context):
			return True
		
		if self.length is None:
			return
		
		ln = len(value)
		length = self.length() if callable(self.length) else self.length
		
		if not isinstance(length, slice) and ln > length:
			raise Concern(ERROR, "Value too long; must be {0} or shorter.", length)
		
		elif ln not in range(*length.indices(ln)):
			raise Concern(ERROR, "Length out of bounds; must be between {0} and {1} long.",
					length.start, length.stop)


class Range(Validator):
	"""Ensure the value is within a given range."""
	
	minimum = Attribute(default=None)
	maximum = Attribute(default=None)
	
	def validate(self, value, context=None):
		if super(Range, self).validate(value, context):
			return True
		
		if self.minimum is None and self.maximum is None:
			return
		
		minimum, maximum = self.minimum, self.maximum
		
		if minimum and maximum and not (minimum <= value <= maximum):
			raise Concern(ERROR, "Out of bounds; must be greater than {0} and less than {1}.",
					minimum, maximum)
		
		elif minimum and value < minimum:
			raise Concern(ERROR, "Too small; must be greater than {0}.", minimum)
		
		elif maximum and value > maximum:
			raise Concern(ERROR, "Too large; must be less than {1}.", maximum)


class Pattern(Validator):
	pattern = Attribute(default=None)  # TODO: Ensure this is always a compiled regex.
	
	def __call__(self, value, context=None):
		if super(Pattern, self).validate(value, context):
			return True
		
		if not self.pattern:
			return
		
		if not self.pattern.match(value):
			raise Concern(ERROR, "Failed to match required pattern.")


class Instance(Validator):
	"""Ensure the value is an instance of the given class."""
	
	instance = Attribute(default=None)
	
	def validate(self, value, context=None):
		if super(InstanceOf, self).validate(value, context):
			return True
		
		if self.instance and not isinstance(value, self.instance):
			raise Concern(ERROR, "Value is not an instance of {0!r}.", self.instance)


class Subclass(Validator):
	"""Ensure the value is a subclass of the given class."""
	
	subclass = Attribute(default=None)
	
	def validate(self, value, context=None):
		if super(Subclass, self).validate(value, context):
			return True
		
		if self.subclass and not issubclass(value, self.subclass):
			raise Concern(ERROR, "Value is not a subclass of {0!r}.", self.subclass)


class Equal(Validator):
	"""Ensure the value being validated equals another.
	
	The value to compare against may be a callback taking no arguments and returning the value for comparison.
	"""
	
	equals = Attribute()
	
	def validate(self, value, context=None):
		if super(Equals, self).validate(value, context):
			return True
		
		# We perform this little dance to ensure None is a valid value.
		try:
			other = self.equals() if callable(self.equals) else self.equals
		except AttributeError:
			return
		
		if value != other:
			raise Concern(ERROR, "Value does not equal: {0}", other)


class Unique(Validator):
	"""Ensure the values of an iterable are unique.
	
	Works on built-in iterables such as lists, tuples, sets, etc. and even dictionaries, though it only checks
	dictionary values as the keys are already gaurenteed to be unique.
	"""
	
	def validate(self, value, context=None):
		if super(Unique, self).validate(value, context):
			return True
		
		value = value.values() if hasattr(value, 'values') else value
		
		if not len(value) == len(set(value)):
			raise Concern(ERROR, "Not all values are unique.")
