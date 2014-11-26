# encoding: utf-8

from __future__ import unicode_literals

from marrow.schema.compat import native, unicode, StringIO
from marrow.schema.exc import Concern
from marrow.schema.testing import ValidationTest

from marrow.schema.transform.base import BaseTransform, Transform, IngressTransform, EgressTransform, SplitTransform


PASSTHROUGH = (None, False, True, "", "Foo", 27, 42.0, [], {})
ST = SplitTransform(
		reader = IngressTransform(ingress=int),
		writer = EgressTransform(egress=unicode)
	)


class TestForeignPassthrough(ValidationTest):
	validator = BaseTransform().foreign
	valid = PASSTHROUGH
	
	def test_loads_none(self):
		assert BaseTransform().loads('') is None
	
	def test_load(self):
		assert BaseTransform().load(StringIO(native("bar"))) == "bar"


class TestNativePassthrough(ValidationTest):
	validator = BaseTransform().native
	valid = PASSTHROUGH
	
	def test_dumps_none(self):
		assert BaseTransform().dumps(None) == ''
	
	def test_dump(self):
		fh = StringIO()
		assert BaseTransform().dump(fh, "baz") == 3
		assert fh.getvalue() == "baz"


class TestTransform(ValidationTest):
	validator = Transform().native
	valid = PASSTHROUGH + ((' foo ', 'foo'), )
	binary = True
	
	def test_decoding(self):
		result = self.validator('Zoë'.encode('utf8'))
		assert isinstance(result, unicode)
		assert result == 'Zoë'


class TestIngress(ValidationTest):
	validator = IngressTransform(ingress=int).native
	valid = (27, ("42", 42), (2.15, 2))
	invalid = ('x', '', [], {})
	binary = True
	
	direction = 'incoming'
	
	def test_concern(self):
		try:
			self.validator('x')
		except Concern as e:
			assert self.direction in unicode(e)
			assert 'invalid literal' in unicode(e)


class TestEgress(TestIngress):
	validator = EgressTransform(egress=int).foreign
	direction = 'outgoing'


class TestSplitTransform(object):
	def test_construction(self):
		try:
			SplitTransform()
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a concern."


class TestSplitTransformReader(ValidationTest):
	validator = ST.native
	valid = (('27', 27), (3.14159, 3), (0.5, 0))
	invalid = TestIngress.invalid + (float('inf'), )
	binary = True
	
	def test_loads_none(self):
		assert ST.loads('') is None
	
	def test_load(self):
		assert ST.load(StringIO(native("42"))) == 42


class TestSplitTransformWriter(ValidationTest):
	validator = ST.foreign
	valid = ((27, '27'), (42, '42'), (3.14, "3.14"))
	binary = True
	
	def test_dumps_none(self):
		assert ST.dumps(None) == ''
	
	def test_dump(self):
		fh = StringIO()
		assert ST.dump(fh, 2.15) == 4
		assert fh.getvalue() == "2.15"
