# encoding: utf-8

from __future__ import unicode_literals

import sys
import copy

from logging import ERROR

from .. import Attribute, Attributes
from .base import Concern, Validator


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
		value = super(Any, self).validate(value, context)
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
		value = super(All, self).validate(value, context)
		
		for validator in self._validators:
			value = validator.validate(value, context)
		
		return value


class Pipe(Compound):
	"""Evaluate multiple validators, requiring all to pass.  Will always evaluate all validators."""
	
	def validate(self, value, context=None):
		value = super(Pipe, self).validate(value, context)
		failures = []
		
		for validator in self._validators:
			try:
				value = validator.validate(value, context)
			except Concern as e:
				failures.append(e)
		
		if failures:
			raise Concern("One or more validators failed.", concerns=failures)
		
		return value
