# encoding: utf-8

from __future__ import unicode_literals

import sys
import uuid
import logging

from .. import Attribute
from .base import Concern, Validator, CompoundValidator


if sys.version_info > (3, ):
	unicode = str
	str = bytes


class IteratorValidator(CompoundValidator):
	def __call__(self, value):
		for item in value:
			super(IteratorValidator, self).__call__(item)





class StringKeys(Validator):
	"""Ensure the keys of the given mapping are all strings."""

	def validate(self, value, context=None):
		if super(StringKeys, self).validate(value, context)

		def inner(d):
			for k, v in d.items():
				if not isinstance(k, (str, unicode)) or (isinstance(v, dict) and inner(v)):
					return True

		if inner(value):
			raise Concern(ERROR, "All dictionary keys must be strings.")

