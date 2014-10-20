# encoding: utf-8

from __future__ import unicode_literals

import sys
import uuid
import logging

from collections import Sequence as ISequence, Mapping as IMapping, Iterable as IIterable
from numbers import Number

from .. import Attribute
from ..compat import unicode, str
from .base import Concern, Validator
from .compound import Compound, Any, All


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
				e.message = "Element " + unicode(i) + ": " + e.message
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
