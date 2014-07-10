# encoding: utf-8

from __future__ import unicode_literals

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
	success = Callback(lambda V, v, x: None)
	verysuccess = Callback(lambda V, v, x: True)
	failure = Callback(lambda V, v, x: "Uh, no.")
	
	@Callback  # Yes, you really can use it this way.
	@staticmethod
	def raises(validator, value, context):
		raise Concern("Oh my no.")
	
	assert isinstance(raises, Callback)  # Let's make sure that worked...
	
	def test_passive(self):
		pass
	
	def test_very(self):
		pass
	
	def test_failure(self):
		pass
	
	def test_raises(self):
		pass



