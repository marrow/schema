# encoding: utf-8

from __future__ import unicode_literals

import re

from marrow.schema.validation.testing import ValidationTest
from marrow.schema.compat import unicode
from marrow.schema.validation.base import *
from marrow.schema.validation.compound import *


length = Length(slice(1, 21))


class CompoundSample(Compound):
	bar = AlwaysRequired()
	foo = Instance(unicode)


class SampleAny(Any, CompoundSample):
	pass


class SampleAll(All, CompoundSample):
	pass


class SamplePipe(Pipe, CompoundSample):
	pass


def test_compound_iteration():
	sample = CompoundSample((length, ))
	assert list(sample._validators) == [sample.bar, sample.foo, length]


class TestAny(ValidationTest):
	validator = SampleAny((length, )).validate
	valid = ('', True, 'Foo')
	invalid = ([], )
	
	def test_total_failure(self):
		try:
			self.validator([])
		except Concern as e:
			assert len(e.concerns) == 3
		else:
			assert False, "Failed to raise a Concern."


class TestAll(ValidationTest):
	validator = SampleAll((length, )).validate
	valid = ('Testing.', )
	invalid = (True, ' ' * 21, ['foo'])
	
	def test_total_failure(self):
		try:
			self.validator([])
		except Concern as e:
			assert not e.concerns, "Must give up on first failure."
		else:
			assert False, "Failed to raise a Concern."


class TestPipe(ValidationTest):
	validator = SamplePipe((length, )).validate
	
	valid = TestAll.valid
	invalid = TestAll.invalid
	
	def _do(self, value, expect):
		try:
			self.validator(value)
		except Concern as e:
			assert len(e.concerns) == expect  # Should collect the failures.
		else:
			assert False, "Failed to raise a Concern."
	
	def test_nested_concerns(self):
		for i, j in ((True, 2), (' ' * 21, 1), (('foo', ) * 21, 2), (['foo'], 1)):
			self._do(i, j)
