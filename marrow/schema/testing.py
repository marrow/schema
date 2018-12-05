"""Utilities for assisting in testing validators.

These are used by Marrow Schema's validation tests and is exported for use in your own.
"""

import pytest

from .exc import Concern


def pytest_generate_tests(metafunc):
	"""Automatically bind valid/invalid class attribute fixtures to the provided test templates.
	
	If you utilize the ValidationTest class or derivatives you will need to either import this fucntion into your test
	module or your test-global `conftest.py` file, or Pytest will complain of missing fixtures.
	"""
	
	if not metafunc.cls:
		return
	
	inst = metafunc.cls()
	
	if 'valid' in metafunc.fixturenames:
		metafunc.parametrize('valid', inst.valid)
	
	if 'invalid' in metafunc.fixturenames:
		metafunc.parametrize('invalid', inst.invalid)


class ValidationTest:
	validator = None
	valid = ()
	invalid = ()
	binary = False
	
	def test_valid_values(self, valid):
		if self.binary and isinstance(valid, tuple) and len(valid) == 2:
			assert self.validator(valid[0]) == valid[1]
		else:
			assert self.validator(valid) == valid
	
	def test_invalid_values(self, invalid):
		with pytest.raises(Concern):
			self.validator(invalid)


class TransformTest(ValidationTest):
	transform = None
	binary = True
	
	@property
	def validator(self):
		return self.transform
