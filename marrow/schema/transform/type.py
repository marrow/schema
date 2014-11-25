# encoding: utf-8

from __future__ import unicode_literals

import sys

from marrow.util.convert import boolean

from .base import Transform, SimpleTransform, Attribute
from ..validation.exc import Concern


if sys.version_info > (3, ):
	unicode = str
	str = bytes


class BooleanTransform(Transform):
	use = Attribute(default=0)  # Which of the pairs to use for the "foreign" side.
	true = Attribute(default=(True, 'yes', 'y', 'on', 'true', 't', '1'))
	false = Attribute(default=(False, 'no', 'n', 'off', 'false', 'f', '0'))
	
	def foreign(self, value, context=None):
		use = self.use
		
		try:
			return self.true[use] if value.strip() else self.false[use]
		except AttributeError:
			return self.true[use] if bool(value) else self.false[use]
	
	def native(self, value, context=None):
		value = super(BooleanTransform, self).native(value, context)
		
		try:
			value = value.strip().lower()
		except AttributeError:
			return bool(input)
		
		if value in self.true:
			return True
		
		if value in self.false:
			return False
		
		raise Concern("Unable to convert {0!r} to a boolean value.", value)

boolean = BooleanTransform()


class BooleanWebTransform(BooleanTransform):
	"""Some web frameworks and widget systems handle checkboxes by having a hidden form field and a checkbox.
	
	If the checkbox is unchecked, you get the "default" value as the only value.  If the checkbox is checked, you end
	up with two values, one for the hidden field (False) and one for the checkbox (True); in this situation we only
	take the last value defined.
	"""
	
	def native(self, value):
		return super(BooleanWebTransform, self).native(value[0] if isinstance(value, (list, tuple)) else value)


class IntegerTransform(SimpleTransform):
	type = int


class FloatTransform(SimpleTransform):
	type = float


class NumberTransform(ChainTransform):
	integer = IntegerTransform()
	floating = FloatTransform()

number = NumberTransform()
