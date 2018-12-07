from marrow.schema.testing import TransformTest

from marrow.schema.transform.type import Boolean, boolean, WebBoolean, web_boolean


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
			yield i, boolean.truthy[boolean.use] if bool(i) else boolean.falsy[boolean.use]
		
		for i in boolean.truthy:
			yield i, boolean.truthy[boolean.use]
		
		for i in boolean.falsy:
			yield i, boolean.falsy[boolean.use]


class TestBooleanNoNoneNative(TransformTest):
	transform = Boolean(none=False).native
	valid = ((None, False), )
	invalid = ('', 'bob')


class TestBooleanNoNoneForeign(TransformTest):
	transform = Boolean(none=False).foreign
	valid = ((None, 'false'), ('foo', 'true'), ('', 'false'))


class TestWebBooleanNative(TransformTest):
	transform = web_boolean.native
	valid = (
			(['', 'true'], True),
			([''], False),
			('', False),
		)


class TestWebBooleanForeign(TransformTest):
	transform = web_boolean.foreign
	valid = [(i, bool(i)) for i in (0, 1, False, True)]
