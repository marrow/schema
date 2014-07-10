# encoding: utf-8

from __future__ import unicode_literals

import re

from marrow.schema.validation.base import *


class TestConstants(object):
	always = Always()
	never = Never()
	
	def test_always(self):
		assert self.always.validate(None) is None
	
	def test_never(self):
		try:
			self.never.validate(True)
		except Concern as e:
			assert unicode(e) == "Set to always fail."


class TestTruthyPresence(object):
	truthes = (True, 'Foo', 1, [None], (None, ), set("abc"))
	falsehoods = (False, '', 0, [], tuple(), set())
	assigned = (True, False, 0, 1, 'abc')
	empty = (None, [], '')
	
	truthy = Truthy(True)
	falsy = Falsy(True)
	required = Required(True)
	missing = Missing(True)
	
	def _do(self, validator, positive, negative):
		for value in positive:
			assert validator.validate(value) == value
		
		for value in negative:
			try:
				validator.validate(value)
			except Concern:
				pass
			else:
				assert False, "Failed to raise a Concern."
	
	def test_true_values(self):
		self._do(self.truthy, self.truthes, self.falsehoods)
	
	def test_false_values(self):
		self._do(self.falsy, self.falsehoods, self.truthes)
	
	def test_required_values(self):
		self._do(self.required, self.assigned, self.empty)
	
	def test_missing_values(self):
		self._do(self.missing, self.empty, self.assigned)


class TestCallbacks(object):
	empty = Callback()
	success = Callback(lambda V, v, x: v)
	failure = Callback(lambda V, v, x: Concern("Uh, no."))
	
	@Callback  # Yes, you really can use it this way.  Implies staticmethod.
	def raises(validator, value, context):
		raise Concern("Oh my no.")
	
	assert isinstance(raises, Callback)  # Let's make sure that worked...
	
	def test_empty(self):
		assert self.empty.validate(27) == 27
	
	def test_success(self):
		assert self.success.validate(None) is None
	
	def test_failure(self):
		try:
			self.failure.validate(None)
		except Concern as e:
			assert unicode(e) == "Uh, no."
		else:
			assert False, "Failed to raise a Concern."
	
	def test_raises(self):
		try:
			self.raises.validate(None)
		except Concern as e:
			assert unicode(e) == "Oh my no."
		else:
			assert False, "Failed to raise a Concern."


class TestIn(object):
	empty = In()
	simple = In([1, 2, 3])
	descriptive = In([(1, "First"), (2, "Second"), (3, "Third")])
	callback = In(lambda: [1, 2, 3])
	
	def _do(self, validator):
		assert validator.validate(1) == 1
		
		try:
			validator.validate(4)
		except Concern as e:
			assert unicode(e) == "Value is not in allowed list."
		else:
			assert False, "Failed to raise a Concern."
	
	def test_empty(self):
		assert self.empty.validate(4) == 4
	
	def test_simple(self):
		self._do(self.simple)
	
	def test_descriptive(self):
		self._do(self.descriptive)
	
	def test_callback(self):
		self._do(self.callback)


class TestContains(object):
	empty = Contains()
	simple = Contains(27)
	callback = Contains(lambda: 42)
	
	def _do(self, validator):
		assert validator.validate([1, 27, 42]) == [1, 27, 42]
		
		try:
			validator.validate([1, 2, 3])
		except Concern as e:
			assert unicode(e).startswith("Value does not contain: ")
		else:
			assert False, "Failed to raise a Concern."
	
	def test_empty(self):
		assert self.empty.validate([4, 20]) == [4, 20]
	
	def test_simple(self):
		self._do(self.simple)
	
	def test_callback(self):
		self._do(self.callback)


class TestLength(object):
	empty = Length()
	simple = Length(20)
	callback = Length(lambda: 10)
	rangeish = Length(slice(5, 15, 2))  # Yup, even step works here.
	exact = Length(slice(32, 33))  # I.e. for an MD5 hash.  L <= v < R
	tupleish = Length((5, 15))  # Won't work for now.  See TODO.
	
	def test_empty(self):
		assert self.empty.validate('') == ''
	
	def _do(self, validator, good, bad):
		assert validator.validate(good) == good
		
		try:
			validator.validate(bad)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
	
	def test_simple(self):
		self._do(self.simple, " " * 5, " " * 25)
	
	def test_callback(self):
		self._do(self.callback, " " * 5, " " * 15)
	
	def test_rangeish(self):
		self._do(self.rangeish, " " * 7, " " * 8)
		self._do(self.rangeish, " " * 11, " " * 4)
		self._do(self.rangeish, " " * 11, " " * 27)
	
	def test_exact(self):
		self._do(self.exact, " " * 32, " " * 31)
		self._do(self.exact, " " * 32, " " * 33)


class TestRange(object):
	empty = Range()
	minonly = Range(5, None)
	maxonly = Range(None, 5)
	minmax = Range(5, 10)
	odd = Range((2,6), (3,4))
	callback = Range(None, lambda: 5)
	
	def _do(self, validator, good, bad):
		assert validator.validate(good) == good
		
		try:
			validator.validate(bad)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
	
	def test_empty(self):
		assert self.empty.validate('') == ''
	
	def test_minimum(self):
		self._do(self.minonly, 10, 3)
		self._do(self.minmax, 5, 4)
	
	def test_maximum(self):
		self._do(self.maxonly, 5, 10)
		self._do(self.minmax, 10, 11)
		self._do(self.minmax, 10, 11)
		self._do(self.callback, 5, 6)
	
	def test_odd(self):
		self._do(self.odd, (2,7), (2,4))
		self._do(self.odd, (3,2), (3,5))
		self._do(self.odd, (3, ), (2, ))


class TestPattern(object):
	empty = Pattern()
	simple = Pattern(r'[a-zA-Z]+')  # TODO: This is a simple string regex.
	simple = Pattern(re.compile(r'^[a-zA-Z]+$'))
	
	def test_empty(self):
		assert self.empty.validate('') == ''
	
	def test_simple(self):
		assert self.simple.validate('foo') == 'foo'
		
		try:
			self.simple.validate('Xyzzy-27!')
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."


class TestInstance(object):
	empty = Instance()
	uni = Instance(unicode)
	
	def test_empty(self):
		assert self.empty.validate('') == ''
	
	def test_uni(self):
		assert self.uni.validate('hello') == 'hello'
		
		try:
			self.uni.validate(27)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."


class TestSubclass(object):
	empty = Subclass()
	valid = Subclass(Validator)
	
	def test_empty(self):
		assert self.empty.validate(object) is object

	def test_valid(self):
		assert self.valid.validate(Subclass) is Subclass

		try:
			self.valid.validate(object)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."


class TestEqual(object):
	empty = Equal()
	equal = Equal(27)
	nil = Equal(None)
	
	def test_empty(self):
		assert self.empty.validate('') == ''
		assert self.empty.validate(None) is None
	
	def test_equal(self):
		assert self.equal.validate(27) == 27
		assert self.equal.validate(27.0) == 27.0
		
		try:
			self.equal.validate('27')
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
	
	def test_nil(self):
		assert self.nil.validate(None) is None
		
		try:
			self.equal.validate(False)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."


class TestUnique(object):
	validator = Unique()
	
	def _do(self, good, bad):
		assert self.validator.validate(good) == good
		
		try:
			self.validator.validate(bad)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
	
	def test_text(self):
		self._do('cafe', 'babe')
	
	def test_list(self):
		self._do([27, 42], [1, 3, 3, 7])
	
	def test_dict(self):
		self._do(dict(bob=27, dole=42), dict(prince=12, pepper=12))
