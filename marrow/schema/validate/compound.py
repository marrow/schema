import sys
import copy

from collections.abc import Sequence as ISequence, Mapping as IMapping, Iterable as IIterable
from numbers import Number

from .. import Attribute, Attributes
from .base import Concern, Validator


# ## Class Definitions

class Compound(Validator):
	"""Allow for syntactically simple control over groups of validators.
	
	Do not use this validator directly; use one of its subclasses instead.
	"""
	
	validators = Attribute(default=None)  # Allow for easy definition at instantiation time.
	
	__validators__ = Attributes(only=Validator)  # Also allow for definition at class construction time.
	
	@property
	def _validators(self):
		"""Iterate across the complete set of child validators."""
		
		for validator in self.__validators__.values():
			yield validator
		
		if self.validators:
			for validator in self.validators:
				yield validator


class Any(Compound):
	"""Evaluate multiple validators, stopping on the first success."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		failures = []
		
		for validator in self._validators:
			try:
				return validator.validate(value, context)
			except Concern as e:
				failures.append(e)
		
		raise Concern("All validators failed.", concerns=failures)


class All(Compound):
	"""Evaluate multiple validators, requiring all to pass.  Stops on the first failure."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		for validator in self._validators:
			value = validator.validate(value, context)
		
		return value


class Pipe(Compound):
	"""Evaluate multiple validators, requiring all to pass.  Will always evaluate all validators."""
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		failures = []
		
		for validator in self._validators:
			try:
				value = validator.validate(value, context)
			except Concern as e:
				failures.append(e)
		
		if failures:
			raise Concern("One or more validators failed.", concerns=failures)
		
		return value


class Iterable(Compound):
	"""Validate that the value is iterable and that the values optionally conform to a schema.
	
	Will attempt to iterate nearly anything.
	"""
	
	require = Attribute(default=All)
	
	def validate(self, value, context=None):
		if not isinstance(value, IIterable):
			raise Concern("Value must be iterable.")
		
		validate = self.require(validators=list(self._validators)).validate
		
		concerns = []
		
		for i, item in enumerate(value):
			try:
				validate(item, context)
			except Concern as e:
				e.message = "Element " + str(i) + ": " + e.message
				concerns.append(e)
		
		if len(concerns) == 1:
			raise concerns[0]
		elif concerns:
			raise Concern(max(i.level for i in concerns), "Multiple validation concerns.", concerns=concerns)
		
		return value


class Mapping(Compound):
	"""Validate that the value is a mapping whose values (not keys) optionally conform to a schema."""
	
	require = Attribute(default=All)
	
	def validate(self, value, context=None):
		if not isinstance(value, IMapping):
			raise Concern("Value must be a mapping.")
		
		validate = self.require(validators=list(self._validators)).validate
		
		concerns = []
		
		for key in value:
			try:
				validate(value[key], context)
			except Concern as e:
				e.message = "Element " + repr(key) + ": " + e.message
				concerns.append(e)
		
		if len(concerns) == 1:
			raise concerns[0]
		elif concerns:
			raise Concern(max(i.level for i in concerns), "Multiple validation concerns.", concerns=concerns)
		
		return value
