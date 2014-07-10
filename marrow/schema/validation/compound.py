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
			for validator in validators:
				yield validator
	
	def validate(self, value, context=None):
		if super(Compound, self).validate(value, context):
			return True
		
		# Exit early if there aren't any...
		if not self.validators and not self.__validators__:
			return True


class Any(Compound):
	"""Evaluate multiple validators, stopping on the first success."""
	
	def validate(self, value, context=None):
		if super(Any, self).validate(value, context):
			return True
		
		for validator in self._validators:
			try:
				return validator.validate(value, context)
			except Concern as e:
				pass  # TODO: Gather the multiple failures... then re-raise them later.
		else:
			raise Concern(ERROR, "All validators failed.")


class All(Compound):
	"""Evaluate multiple validators, requiring all to pass.  Stops on the first failure."""
	
	def validate(self, value, context=None):
		if super(All, self).validate(value, context):
			return True
		
		for validator in self._validators:
			validator.validate(value, context)
