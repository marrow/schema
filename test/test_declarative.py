# encoding: utf-8

import pytest

from marrow.schema.declarative import Container, DataAttribute, Attribute


class TestContainer:
	class Sample(Container):
		foo = Attribute(default=None)
		bar = Attribute(default=None)
	
	def test_container_keyword_arguments(self):
		instance = self.Sample(foo=27, bar=42)
		assert instance.foo == 27
		assert instance.bar == 42
	
	def test_container_unknown_keyword(self):
		try:
			self.Sample(baz=None)
		except TypeError:
			pass
	
	def test_container_positional_arguments(self):
		instance = self.Sample(27, 42)
		assert instance.foo == 27
		assert instance.bar == 42
	
	def test_container_too_many_positional(self):
		try:
			self.Sample(1, 2, 3)
		except TypeError:
			pass
	
	def test_container_argument_conflict(self):
		try:
			self.Sample(1, foo=2)
		except TypeError:
			pass
	
	def test_container_mixed_arguments(self):
		instance = self.Sample(27, bar=42)
		assert instance.foo == 27
		assert instance.bar == 42


class TestDataAttribute:
	class Sample(Container):
		foo = DataAttribute()
	
	def test_get_attribute(self):
		assert self.Sample.foo.__class__ is DataAttribute
	
	def test_get_unassigned(self):
		instance = self.Sample()
		
		try:
			instance.foo
		except AttributeError:
			pass
	
	def test_storage(self):
		instance = self.Sample(27)
		assert instance.__data__ == dict(foo=27)
		
		instance.foo = 42
		assert instance.__data__ == dict(foo=42)
	
	def test_retrieval(self):
		instance = self.Sample()
		instance.__data__['foo'] = 27
		assert instance.foo == 27
	
	def test_deletion(self):
		instance = self.Sample(27)
		del instance.foo
		assert instance.__data__ == dict()


class TestAttribute:
	class Sample(Container):
		foo = Attribute()
		bar = Attribute(default=42)
		baz = Attribute('bazzy')
		diz = Attribute(default=lambda: 27)
	
	def test_direct_access(self):
		assert self.Sample.foo.__class__ is Attribute
	
	def test_empty(self):
		instance = self.Sample()
		assert instance.__data__ == dict()
	
	def test_default(self):
		instance = self.Sample()
		assert instance.bar == 42
		assert instance.diz == 27
		assert instance.__data__ == dict()
		
		# We monkeypatch a value here; you're meant to do this through subclassing.
		self.Sample.bar.assign = True
		instance.bar
		assert instance.__data__ == dict(bar=42)
		self.Sample.bar.assign = False
	
	def test_nodefault(self):
		instance = self.Sample()
		
		try:
			instance.foo
		except AttributeError:
			pass
	
	def test_assignment(self):
		instance = self.Sample()
		instance.foo = 42
		instance.bar = 27
		assert instance.__data__ == dict(foo=42, bar=27)
	
	def test_deletion(self):
		instance = self.Sample(27, 16)
		assert instance.__data__ == dict(foo=27, bar=16)
		del instance.bar
		assert instance.bar == 42
		assert instance.__data__ == dict(foo=27)
	
	def test_othername(self):
		instance = self.Sample(baz="Hello, world!")
		assert instance.__data__ == dict(bazzy="Hello, world!")
