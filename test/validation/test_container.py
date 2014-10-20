# encoding: utf-8

from __future__ import unicode_literals

import re

from marrow.schema.compat import unicode
from marrow.schema.validation.base import truthy, falsy, Instance
from marrow.schema.validation.exc import Concern
from marrow.schema.validation.testing import ValidationTest
from marrow.schema.validation.container import *


INVALID = (None, 1, True)
EMPTY = (tuple(), list(), dict(), "")
STRINGS = (('a', 'b'), ['a', 'b'], {'a': "one", 'b': "two"}, set(['a', 'b']), "foo")
INTEGERS = ((0, 1, 2), [0, 1, 2], {0: 0, 1: 1, 2: 2}, set([0, 1, 2]))
TRUTHY = ((1, True, 'foo'), [1, True, 'foo'], {'a': 1, 'b': True, 1: 'foo'}, set([1, True, 'foo']))
FALSY = ((0, False, ''), [0, False, ''], {None: 0, '': False, 0: ''}, set([0, False, '']))


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
		stringy = Instance(unicode)
	
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
			print(e.concerns)
			assert "Element 1" in e.concerns[1].message, "Should identify element failing validation."
