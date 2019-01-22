import re

from marrow.schema.testing import ValidationTest
from marrow.schema.validate.base import AlwaysRequired, Instance, Length, falsy, truthy, Concern
from marrow.schema.validate.compound import All, Any, Compound, Iterable, Mapping, Pipe


length = Length(slice(1, 21))


class CompoundSample(Compound):
	bar = AlwaysRequired()
	foo = Instance(str)


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


# For validation of iterables.

INVALID = (None, 1, True)
EMPTY = (tuple(), list(), dict(), "")
STRINGS = (('a', 'b'), ['a', 'b'], {'a': "one", 'b': "two"}, set(['a', 'b']), "foo")
INTEGERS = ((0, 1, 2), [0, 1, 2], {0: 0, 1: 1, 2: 2}, set([0, 1, 2]))
TRUTHY = ((1, True, 'foo'), [1, True, 'foo'], {'a': 1, 'b': True, 1: 'foo'}, set([1, True, 'foo']))
FALSY = ((0, False, ''), [0, False, ''], {None: 0, '': False, 0: ''}, set([0, False, '']))
NONMAP = (tuple(), list(), "")


class TestIterable(ValidationTest):
	validator = Iterable().validate
	valid = EMPTY + STRINGS + INTEGERS + TRUTHY + FALSY
	invalid = INVALID


class TestTruthyIterable(ValidationTest):
	validator = Iterable([truthy]).validate
	valid = EMPTY + TRUTHY + STRINGS
	invalid = INVALID + FALSY + INTEGERS


class TestFalsyIterable(ValidationTest):
	validator = Iterable([falsy]).validate
	valid = EMPTY + FALSY
	invalid = INVALID + TRUTHY


class TestStringyIterable(ValidationTest):
	class Validator(Iterable):
		stringy = Instance(str)
	
	validator = Validator().validate
	valid = EMPTY + STRINGS
	invalid = INVALID + INTEGERS + TRUTHY + FALSY


class TestIterableConcerns(object):
	def test_singular_failure(self):
		try:
			Iterable([truthy]).validate([True, False])
		except Concern as e:
			assert "Element 1" in e.message, "Should identify element failing validation."
			assert not e.concerns, "Should not contain child concerns."
	
	def test_multiple_failure(self):
		try:
			Iterable([truthy]).validate([0, False])
		except Concern as e:
			assert "multiple" in e.message.lower(), "Should indicate multiple failures."
			assert "Element 1" in e.concerns[1].message, "Should identify element failing validation."


class TestMapping(ValidationTest):
	validator = Mapping([Instance(str)]).validate
	valid = ({}, {1: 'foo', 2: 'bar'})
	invalid = INVALID + NONMAP + ({1: 2, 2: 'baz'}, )


class TestMappingConcerns(object):
	def test_singular_failure(self):
		try:
			Mapping([truthy]).validate({'bob': True, 'dole': False})
		except Concern as e:
			assert "dole" in e.message, "Should identify element failing validation."
			assert not e.concerns, "Should not contain child concerns."
	
	def test_multiple_failure(self):
		try:
			Mapping([truthy]).validate({'bob': False, 'dole': False})
		except Concern as e:
			assert "multiple" in e.message.lower(), "Should indicate multiple failures."
			assert "dole" in e.concerns[0].message or "dole" in e.concerns[1].message, "Should identify element failing validation."
