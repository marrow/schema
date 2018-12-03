from marrow.schema.testing import TransformTest

from marrow.schema.transform.container import Array, array


PAK = "foo,bar"
ARRAYS = (None, [], [0, 1, '', 2, 3], PAK, "foo ,bar", "foo,,bar", "foo, bar")
TWO = ['foo', 'bar']
TTWO = tuple(TWO)
THREE = ['foo', '', 'bar']
LSPC = ['foo ', 'bar']
RSPC = ['foo', ' bar']


class TestArrayDefaultNative(TransformTest):
	transform = array.native
	valid = zip(ARRAYS, ([], [], ['0', '1', '2', '3'], TWO, TWO, TWO, TWO))


class TestArrayDefaultForeign(TransformTest):
	transform = array.foreign
	valid = [(i, PAK) for i in (TWO, THREE, LSPC, RSPC)] + [('bob', 'b,o,b'), ]


class TestArrayEmptyNative(TransformTest):
	transform = Array(empty=True).native
	valid = zip(ARRAYS, ([], [], ['0', '1', '', '2', '3'], TWO, TWO, THREE, TWO))


class TestArrayEmptyForeign(TransformTest):
	transform = Array(empty=True).foreign
	valid = [(i, PAK) for i in (TWO, LSPC, RSPC)] + [(THREE, 'foo,,bar'), ]


class TestArraySeparatorNative(TransformTest):
	transform = Array(separator='|').native
	valid = [(i, TWO) for i in ('foo|bar', 'foo |bar', 'foo||bar')]


class TestArrayNoStrip(TransformTest):
	transform = Array(strip=False).native
	valid = (('foo, bar', TWO), ('foo , bar', LSPC), ('foo,  bar', RSPC))


class TestArrayNoSepNative(TransformTest):
	transform = Array(separator=None).native
	valid = (('foo bar', TWO), ('foo  bar', TWO))


class TestArrayNoSepForeign(TransformTest):
	transform = Array(separator=None).foreign
	valid = ((TWO, 'foo bar'), (THREE, 'foo bar'))


class TestArrayCast(TransformTest):
	transform = Array(cast=tuple).native
	valid = zip(ARRAYS, (tuple(), tuple(), ('0', '1', '2', '3'), TTWO, TTWO, TTWO, TTWO))


class TestArrayBoomNative(TransformTest):
	transform = Array(cast=lambda a: 1/0).native
	invalid = ('', )


class TestArrayBoomForeign(TransformTest):
	transform = Array(separator=27).foreign
	invalid = ([], )
