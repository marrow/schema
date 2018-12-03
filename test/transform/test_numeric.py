from marrow.schema.testing import TransformTest

from marrow.schema.transform.type import Integer, integer, Decimal, decimal, Number, number


INTS = ('1', '5', '-27')
FLOTS = ('1.5', '-27.0', '0.0', '-0.0')
INV = ('a', 'fourty two', '0x27')


class TestIntegerNative(TransformTest):
	transform = integer.native
	valid = tuple((i, int(i)) for i in INTS)
	invalid = INV


class TestIntegerForeign(TransformTest):
	transform = integer.foreign
	valid = tuple((int(i), i) for i in INTS)


class TestDecimalNative(TransformTest):
	transform = decimal.native
	valid = tuple((i, float(i)) for i in FLOTS)
	invalid = INV


class TestDecimalForeign(TransformTest):
	transform = decimal.foreign
	valid = tuple((float(i), i) for i in FLOTS)


class TestNumberNative(TransformTest):
	transform = number.native
	valid = tuple((i, int(i)) for i in INTS) + tuple((i, float(i)) for i in FLOTS)
	invalid = INV


class TestNumberForeign(TransformTest):
	transform = number.foreign
	valid = tuple((int(i), i) for i in INTS) + tuple((float(i), i) for i in FLOTS)
