# encoding: utf-8

import pytest

from marrow.schema.meta import ElementMeta, Element


def test_element_sequence():
	ElementMeta.sequence = 0
	
	first = Element()
	second = Element()
	
	assert first.__sequence__ == 0
	assert second.__sequence__ == 1
	assert ElementMeta.sequence == 2


def test_element_attributes():
	class TestElement(Element):
		foo = Element()
		bar = Element()
	
	assert list(TestElement.__attributes__.keys()) == ['foo', 'bar']


def test_element_name():
	class TestElement(Element):
		foo = Element()
		bar = Element()
	
	assert TestElement.foo.__name__ == 'foo'
	assert TestElement.bar.__name__ == 'bar'


def test_element_hardcoding():  # Issue #5: https://github.com/marrow/marrow.schema/issues/5
	class TestElement(Element):
		foo = Element()
		bar = Element()
	
	class ElementSubclass(TestElement):
		bar = 27
	
	assert len(TestElement.__attributes__) == 2
	assert ElementSubclass.__attributes__ == dict(foo=TestElement.foo)


def test_element_preserve_order():  # Issue #1: https://github.com/marrow/marrow.schema/issues/1
	class TestElement(Element):
		foo = Element()
		bar = Element()
	
	class ElementSubclass(TestElement):
		foo = Element()
	
	assert ElementSubclass.foo is not TestElement.foo
	assert ElementSubclass.foo.__sequence__ == TestElement.foo.__sequence__
	assert ElementSubclass.__attributes__.keys() == TestElement.__attributes__.keys()


def test_element_inclusion_callbacks():  # Issue #7: https://github.com/marrow/marrow.schema/issues/7
	class ElementSubclass(Element):
		called = False
		
		def __fixup__(self, cls):
			self.called = True
	
	class TestElement(Element):
		foo = ElementSubclass()
	
	assert TestElement.foo.called


def test_element_construction_callback():  # Issue #7: https://github.com/marrow/marrow.schema/issues/7
	class TestElement(Element):
		called = False
		
		@classmethod
		def __attributed__(cls):
			cls.called = True
	
	assert TestElement.called