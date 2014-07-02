# encoding: utf-8

import pytest

from marrow.schema.declarative import Container, Attribute
from marrow.schema.util import Attributes


class SpecialAttribute(Attribute):
	pass


class Sample(Container):
	foo = Attribute()
	bar = SpecialAttribute()
	
	all = Attributes()
	special = Attributes(only=SpecialAttribute)


def test_attributes_access():
	attrs = Sample.all
	
	assert len(attrs) == 4
	assert attrs['foo'] is Sample.foo
	assert attrs['bar'] is Sample.bar


def test_all_attributes():
	instance = Sample()
	
	attrs = instance.all
	
	assert len(attrs) == 4
	assert attrs['foo'] is Sample.foo
	assert attrs['bar'] is Sample.bar


def test_special_attributes():
	assert len(Sample.special) == 1
	assert 'bar' in Sample.special
