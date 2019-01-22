import re

from marrow.schema import Attribute, Concern, Container
from marrow.schema.testing import ValidationTest
from marrow.schema.validate.base import Always, Callback, Contains, Equal, Falsy, In, Instance, Length, Missing, \
		Never, Pattern, Range, Required, Subclass, Truthy, Unique, Validated, Validator


class TestAlways(ValidationTest):
	validator = Always().validate
	valid = (None, False, True, 0, 1, 3.14, '', 'foo', [], ['bar'], {}, {'baz': 'diz'})


class TestNever(ValidationTest):
	validator = Never().validate
	invalid = TestAlways.valid


class TestTruthy(ValidationTest):
	validator = Truthy(True).validate
	valid = (True, 'Foo', 1, [None], (None, ), set("abc"))
	invalid = (False, '', 0, [], tuple(), set())


class TestFalsy(ValidationTest):
	validator = Falsy(True).validate
	valid = TestTruthy.invalid
	invalid = TestTruthy.valid


class TestRequired(ValidationTest):
	validator = Required(True).validate
	valid = (True, False, 0, 1, 'abc')
	invalid = (None, [], '')


class TestMissing(ValidationTest):
	validator = Missing(True).validate
	valid = TestRequired.invalid
	invalid = TestRequired.valid


class TestEmptyCallback(ValidationTest):
	validator = Callback().validate
	valid = TestTruthy.valid + TestTruthy.invalid


class TestSuccessCallback(ValidationTest):
	validator = Callback(lambda V, v, x: v).validate
	valid = TestEmptyCallback.valid


class TestFailureCallback(ValidationTest):
	validator = Callback(lambda V, v, x: Concern("Uh, no.")).validate
	invalid = TestSuccessCallback.valid


class TestCallbacks(object):
	@Callback  # Yes, you really can use it this way.  Implies staticmethod.
	def raises(validator, value, context):
		raise Concern("Oh my no.")
	
	assert isinstance(raises, Callback)  # Let's make sure that worked...
	
	def test_raises(self):
		try:
			self.raises.validate(None)
		except Concern as e:
			assert str(e) == "Oh my no."
		else:
			assert False, "Failed to raise a Concern."


class TestInAny(ValidationTest):
	validator = In().validate
	valid = TestAlways.valid


class TestInSimple(ValidationTest):
	validator = In([1, 2, 3]).validate
	valid = (1, 2, 3)
	invalid = (None, 0, 4, 'bob')


class TestInDescriptive(ValidationTest):
	validator = In([(1, "First"), (2, "Second"), (3, "Third")]).validate
	valid = TestInSimple.valid
	invalid = TestInSimple.invalid


class TestInCallback(ValidationTest):
	validator = In(lambda: [1, 2, 3]).validate
	valid = TestInSimple.valid
	invalid = TestInSimple.invalid


class TestContains(object):
	empty = Contains()
	simple = Contains(27)
	callback = Contains(lambda: 42)
	
	def _do(self, validator):
		assert validator.validate([1, 27, 42]) == [1, 27, 42]
		
		try:
			validator.validate([1, 2, 3])
		except Concern as e:
			assert str(e).startswith("Value does not contain: ")
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
		self._do(self.simple, ('', ) * 5, None)
	
	def test_callback(self):
		self._do(self.callback, " " * 5, " " * 15)
	
	def test_rangeish(self):
		self._do(self.rangeish, " " * 7, " " * 8)
		self._do(self.rangeish, " " * 11, " " * 4)
		self._do(self.rangeish, " " * 11, " " * 27)
		self._do(self.rangeish, ('', ) * 5, None)
	
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
	uni = Instance(str)
	
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


class TestValidated(ValidationTest):
	class Sample(Container):
		foo = Validated(validator=Equal(27))
	
	def test_pass(self):
		inst = self.Sample(27)
		assert inst.foo == 27
		
		inst = self.Sample()
		inst.foo = 27
	
	def test_fail(self):
		try:
			self.Sample(42)
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
		
		inst = self.Sample()
		
		try:
			inst.foo = 42
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a Concern."
