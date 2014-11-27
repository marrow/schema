# encoding: utf-8

from __future__ import unicode_literals

from marrow.schema.compat import native, unicode, StringIO
from marrow.schema.exc import Concern
from marrow.schema.testing import TransformTest

from marrow.schema.transform.complex import Boolean, boolean, Array, array


class TestBooleanNative(TransformTest):
	transform = boolean.native
	invalid = ('x', )
	
	@property
	def valid(self):
		yield None, None
		
		if boolean.none:
			yield '', None
		
		for i in boolean.truthy + ('Y', 'True', True, 1, ['foo']):
			yield i, True
		
		for i in boolean.falsy + ('n', 'False', False, 0, []):
			yield i, False


class TestBooleanForeign(TransformTest):
	transform = boolean.foreign
	
	@property
	def valid(self):
		if boolean.none:
			yield None, ''
		
		for i in (0, 1, False, True, [], [0]):
			yield i, boolean.truthy[0] if bool(i) else boolean.falsy[0]
		
		for i in boolean.truthy:
			yield i, boolean.truthy[0]
		
		for i in boolean.falsy:
			yield i, boolean.falsy[0]


class TestBooleanNoNoneNative(TransformTest):
	transform = Boolean(none=False).native
	valid = ((None, False), )
	invalid = ('', 'bob')


class TestBooleanNoNoneForeign(TransformTest):
	transform = Boolean(none=False).foreign
	valid = ((None, 'false'), ('foo', 'true'), ('', 'false'))


PAK = "foo,bar"
ARRAYS = (None, [], [0, 1, '', 2, 3], PAK, "foo ,bar", "foo,,bar", "foo, bar")
# "foo|bar", "foo |bar", "foo||bar", "foo bar", "foo  bar"

TWO = ['foo', 'bar']
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


TTWO = tuple(TWO)

class TestArrayCast(TransformTest):
	transform = Array(cast=tuple).native
	valid = zip(ARRAYS, (tuple(), tuple(), ('0', '1', '2', '3'), TTWO, TTWO, TTWO, TTWO))


class TestArrayBoomNative(TransformTest):
	transform = Array(cast=lambda a: 1/0).native
	invalid = ('', )


class TestArrayBoomForeign(TransformTest):
	transform = Array(separator=27).foreign
	invalid = ([], )


class foo(object):
	def test_keyword_parser_regex(self):
		self.assertEqual(conv.tags.pattern, '[\\s \t,]*("[^"]+"|\'[^\']+\'|[^ \t,]+)[ \t,]*')
		self.assertEqual(conv.terms.pattern, '[\\s \t]*([+-]?"[^"]+"|\'[^\']+\'|[^ \t]+)[ \t]*')
	
	def test_tags(self):
		self.assertEqual(
				conv.tags('"high altitude" "Melting Panda" panda bends'),
				set(('bends', 'high altitude', 'melting panda', 'panda'))
			)
	
	def test_tag_join(self):
		tags = conv.tags('"high altitude" "melting panda" panda bends')
		self.assertEqual(conv.tags(tags), 'panda "high altitude" bends "melting panda"')
	
	def test_quoteless_join(self):
		tagger = conv.KeywordProcessor(' ', None)
		tags = tagger('panda bends')
		self.assertEqual(tagger(tags), 'panda bends')
	
	def test_terms(self):
		self.assertEqual(
				conv.terms('animals +cat -dog +"medical treatment"'),
				(['animals'], ['cat', '"medical treatment"'], ['dog'])
			)
		
		self.assertEqual(
				conv.terms('animal medicine +cat +"kitty death"'),
				(['animal', 'medicine'], ['cat', '"kitty death"'], [])
			)
		
		conv.terms.group = dict
		self.assertEqual(
				conv.terms(' foo  bar "baz"diz	   '),
				{None: ['foo', 'bar', '"baz"', 'diz'], '+': [], '-': []}
			)
		
		conv.terms.group = False 
		self.assertEqual(
				conv.terms('cat dog -leather'),
				[(None, 'cat'), (None, 'dog'), ('-', 'leather')]
			)