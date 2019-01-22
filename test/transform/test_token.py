from marrow.schema.testing import TransformTest

from marrow.schema.transform.complex import TokenPatternAttribute, Token, tags, terms


class TestTokenGeneral(object):
	def test_token_pattern_cache(self):
		assert 'pattern' not in tags.__data__
		
		pattern, regex = tags.pattern
		
		assert 'pattern' in tags.__data__
	
	def test_tag_pattern(self):
		pattern, regex = tags.pattern
		assert pattern == '[\\s \t,]*("[^"]+"|\'[^\']+\'|[^ \t,]+)[ \t,]*'
	
	def test_term_pattern(self):
		pattern, regex = terms.pattern
		assert pattern == '[\\s \t]*([+-]?"[^"]+"|\'[^\']+\'|[^ \t]+)[ \t]*'
	
	def test_direct_access(self):
		assert isinstance(Token.pattern, TokenPatternAttribute)


class TestTagNative(TransformTest):
	transform = tags.native
	valid = (
			(None, None),
			('', set()),
			('high altitude melting pandas', set(('high', 'altitude', 'melting', 'pandas'))),
			('"high altitude" "melting panda"', set(('high altitude', 'melting panda'))),
			('Melting PANDAS', set(('melting', 'pandas')))
		)


class TestTagForeign(TransformTest):
	transform = tags.foreign
	valid = (
			(None, None),
			(('high', 'altitude'), "high altitude"),
			(('high', 'altitude', 'melting pandas'), 'high altitude "melting pandas"')
		)
	invalid = (
			'',
		)


class TestTermsNative(TransformTest):
	transform = terms.native
	valid = (
			('animals +cat -dog +"medical treatment"', {None: ['animals'], '+': ['cat', '"medical treatment"'], '-': ['dog']}),
		)


class TestTermLikeTuple(TransformTest):
	transform = Token(groups=[None, '+', '-'], group=tuple).native
	valid = (
			('animal medicine +cat +"kitty death"', (['animal', 'medicine'], ['cat', '"kitty death"'], [])),
		)


class TestTermLikeUngrouped(TransformTest):
	transform = Token(groups=[None, '+', '-'], group=None).native
	valid = (
			('cat dog -leather', [(None, 'cat'), (None, 'dog'), ('-', 'leather')]),
		)

class TestTokenSorted(TransformTest):
	transform = Token(separators=' \t,', normalize=lambda s: s.lower().strip('"'), sort=True).native
	valid = (
			('foo bar baz', ['bar', 'baz', 'foo']),
		)

class TestTokenNoQuote(TransformTest):
	transform = Token(quotes=None).foreign
	valid = (
			(("foo", "bar", "baz diz"), "foo bar baz diz"),
		)

class TestTokenDictionaryForeign(TransformTest):
	transform = Token(group=dict, sort=True).foreign
	valid = (
			({'+': ('foo', 'bar'), '-': ('baz', )}, "+bar +foo -baz"),
		)
	invalid = (
			'foo'
		)
	
	'''
		if self.group is dict:
			if not isinstance(value, dict):
				raise Concern("Dictionary grouped values must be passed as a dictionary.")
			
			return self.separators[0].join([(prefix + sanatize(keyword)) for prefix, keywords in value for keyword in value[prefix]])
		
		if not isinstance(value, (list, tuple, set)):
			raise Concern("Ungrouped values must be passed as a list, tuple, or set.")
		
		value = [sanatize(keyword) for keyword in value]
		
		return self.separators[0].join(sorted(value) if self.sort else value)
	'''
