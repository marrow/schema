# encoding: utf-8

from __future__ import unicode_literals

import sys
import uuid
import logging

from collections import Sequence
from numbers import Number

from .. import Attribute
from ..compat import unicode, str
from .base import Concern, Validator
from .compound import Compound, Any, All




class Iterable(Compound):
	"""The sub-elements of the given iterable value must conform to certain criteria."""
	
	require = Attribute(default=All)
	
	def validate(self, value, context=None):
		if not isinstance(value, Sequence):
			raise Concern("Value must be a sequence of items.")
		
		if hasattr(value, 'iteritems'):
			value = value.iteritems()
		elif hasattr(value, 'items'):
			value = value.items()
		else:
			value = enumerate(value)
		
		validate = self.require(validators=self._validators).validate
		concerns = []
		
		for i, item in value:
			try:
				validate(item, context)
			except Concern as e:
				e.message = "Element {0!r}: ".format(i)
				concerns.append(e)
		
		if concerns:
			if len(concerns) == 1:
				raise concerns[0]
			
			raise Concern(max(i.level for i in concerns), "Multiple validation failures.", concerns=concerns)
		
		return value





class StringKeys(Validator):
	"""Ensure the keys of the given mapping are all strings."""

	def validate(self, value, context=None):
		if super(StringKeys, self).validate(value, context):
			pass

		def inner(d):
			for k, v in d.items():
				if not isinstance(k, (str, unicode)) or (isinstance(v, dict) and inner(v)):
					return True

		if inner(value):
			raise Concern(ERROR, "All dictionary keys must be strings.")

