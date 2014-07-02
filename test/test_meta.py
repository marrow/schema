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
