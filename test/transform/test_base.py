from io import StringIO

from marrow.schema.exc import Concern
from marrow.schema.testing import TransformTest

from marrow.schema.transform.base import BaseTransform, Transform, IngressTransform, EgressTransform, SplitTransform


PASSTHROUGH = (None, False, True, "", "Foo", 27, 42.0, [], {})
ST = SplitTransform(
		reader = IngressTransform(ingress=int),
		writer = EgressTransform(egress=str)
	)


class TestForeignPassthrough(TransformTest):
	transform = BaseTransform().foreign
	valid = PASSTHROUGH
	
	def test_loads_none(self):
		assert BaseTransform().loads('') is None
	
	def test_load(self):
		assert BaseTransform().load(StringIO(str("bar"))) == "bar"


class TestNativePassthrough(TransformTest):
	transform = BaseTransform().native
	valid = PASSTHROUGH
	
	def test_dumps_none(self):
		assert BaseTransform().dumps(None) == ''
	
	def test_dump(self):
		fh = StringIO()
		assert BaseTransform().dump(fh, "baz") == 3
		assert fh.getvalue() == "baz"


class TestTransform(TransformTest):
	transform = Transform().native
	valid = PASSTHROUGH + ((' foo ', 'foo'), )
	
	def test_decoding(self):
		result = self.transform('Zoë'.encode('utf8'))
		assert isinstance(result, str)
		assert result == 'Zoë'


class TestIngress(TransformTest):
	transform = IngressTransform(ingress=int).native
	valid = (27, ("42", 42), (2.15, 2))
	invalid = ('x', '', [], {})
	
	direction = 'incoming'
	
	def test_concern(self):
		try:
			self.transform('x')
		except Concern as e:
			assert self.direction in str(e)
			assert 'invalid literal' in str(e)


class TestEgress(TestIngress):
	transform = EgressTransform(egress=int).foreign
	direction = 'outgoing'


class TestSplitTransform(object):
	def test_construction(self):
		try:
			SplitTransform()
		except Concern as e:
			pass
		else:
			assert False, "Failed to raise a concern."


class TestSplitTransformReader(TransformTest):
	transform = ST.native
	valid = (('27', 27), (3.14159, 3), (0.5, 0))
	invalid = TestIngress.invalid + (float('inf'), )
	
	def test_loads_none(self):
		assert ST.loads('') is None
	
	def test_load(self):
		assert ST.load(StringIO(str("42"))) == 42


class TestSplitTransformWriter(TransformTest):
	transform = ST.foreign
	valid = ((27, '27'), (42, '42'), (3.14, "3.14"))
	
	def test_dumps_none(self):
		assert ST.dumps(None) == ''
	
	def test_dump(self):
		fh = StringIO()
		assert ST.dump(fh, 2.15) == 4
		assert fh.getvalue() == "2.15"
