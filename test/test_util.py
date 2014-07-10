# encoding: utf-8

from marrow.schema.declarative import Container, Attribute
from marrow.schema.util import Attributes, ensure_tuple


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


def test_ensure_tuples():
	a = [(1, ), (2, 3), (3, 4, 5), "foo"]
	b = list(ensure_tuple(2, a))  # typically not cast to a list, 'in' or iteration is more usual
	
	assert len(b) == len(a)
	
	for i in b:
		assert len(i) == 2
	
	assert b[0] == (1, 1)
	assert b[1] == (2, 3)
	assert b[2] == (3, 4)
	assert b[3] == ("foo", "foo")
