# encoding: utf-8

from __future__ import unicode_literals

import sys
import copy

from logging import ERROR

from .. import Container, Attribute, Attributes
from .base import Validator


class HasAny(Validator):
	"""Ensure that at least one of the specified fields is defined."""
	
	fields = Attribute()
	
	pass  # TODO


class HasAll(Validator):
	"""Ensure that all of the specified fields are defined."""
	
	fields = Attribute()
	
	pass  # TODO


class Same(Validator):
	"""Ensure the value being validated is the same as another value from the context.

	Useful for things like forms with password verification.
	"""

	other = Attribute(default=None)

	def validate(self, value, context):
		if super(Same, self).validate(value, context):
			return True
		
		pass  # TODO


class Pair(Validator):
	"""Ensure another value is present in the context if the value being validated is present."""
	
	other = Attribute(default=None)
	
	def validate(self, value, context):
		if super(Pair, self).validate(value, context):
			return True
		
		pass  # TODO

