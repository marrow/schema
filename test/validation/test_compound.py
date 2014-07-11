# encoding: utf-8

from __future__ import unicode_literals

import re

from marrow.schema.compat import unicode
from marrow.schema.validation.base import *
from marrow.schema.validation.compound import *


class CompoundSample(Compound):
	bar = AlwaysRequired()
	foo = Instance(unicode)

length = Length(slice(1, 21))

sample = CompoundSample((length, ))


def test_compound_iteration():
	assert list(sample._validators) == [sample.bar, sample.foo, length]


class TestAny(object):
	class SampleAny(Any, CompoundSample):
		pass
	
	sample = SampleAny((length, ))
	
	def test_success(self):
		# Because this only requires that a single condition pass, you might get unexpected allowable results.
		assert self.sample.validate('') == ''
		assert self.sample.validate(True) is True
		assert self.sample.validate('Foo') == 'Foo'
	
	def test_failure(self):
		try:
			self.sample.validate([])
		except Concern as e:
			assert len(e.concerns) == 3
		else:
			assert False, "Failed to raise a Concern."


class TestAll(object):
	class SampleAll(All, CompoundSample):
		pass

	sample = SampleAll((length, ))

	def test_success(self):
		assert self.sample.validate('Testing.') == 'Testing.'

	def _do(self, value, expect):
		try:
			self.sample.validate(value)
		except Concern as e:
			assert not e.concerns  # Must give up on first failure.
		else:
			assert False, "Failed to raise a Concern."

	def test_failure(self):
		for i, j in ((True, 2), (' ' * 21, 1), (['foo'], 2)):
			self._do(i, j)


class TestPipe(object):
	class SamplePipe(Pipe, CompoundSample):
		pass
	
	sample = SamplePipe((length, ))
	
	def test_success(self):
		assert self.sample.validate('Testing.') == 'Testing.'
	
	def _do(self, value, expect):
		try:
			self.sample.validate(value)
		except Concern as e:
			assert len(e.concerns) == expect  # Should collect the failures.
		else:
			assert False, "Failed to raise a Concern."
	
	def test_failure(self):
		for i, j in ((True, 2), (' ' * 21, 1), (('foo', ) * 21, 2), (['foo'], 1)):
			self._do(i, j)








#	def _do(self, validator, positive, negative):
#		for value in positive:
#			assert validator.validate(value) == value
#
#		for value in negative:
#			try:
#				validator.validate(value)
#			except Concern:
#				pass
#			else:
#				assert False, "Failed to raise a Concern."
