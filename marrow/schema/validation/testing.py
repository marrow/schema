# encoding: utf-8

"""Utilities for assisting in testing validators.

These are used by Marrow Schema's validation tests and is exported for use in your own.
"""

from .exc import Concern


class ValidationTest(object):
	validator = None
	valid = ()
	invalid = ()
	
	def test_values(self):
		for value in self.valid:
			yield self._do_valid, value
		
		for value in self.invalid:
			yield self._do_invalid, value
	
	def _do_valid(self, value):
		assert self.validator(value) == value
	
	def _do_invalid(self, value):  # pragma: no cover
		try:
			self.validator(value)
		except Concern:
			pass
		else:
			assert False, "Failed to raise a Concern: " + repr(value)
