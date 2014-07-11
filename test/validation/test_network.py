# encoding: utf-8

from marrow.schema.validation.exc import Concern
from marrow.schema.validation.network import *


class TestMACs(object):
	good = [
			'3D:F2:C9:A6:B3:4F',
			'3d:f2:c9:a6:b3:4f',
			'3D-F2-C9-A6-B3-4F',
		]
	
	bad = [
			'3D:F2:AC9:A6:B3:4F',
			'3D:F2:C9:A6:B3:4F:00',
			':F2:C9:A6:B3:4F',
			'F2:C9:A6:B3:4F',
			'3D-F2:C9-A6:B3-4F',
		]
	
	def _do_success(self, value):
		assert mac.validate(value) == value
	
	def _do_failure(self, value):
		try:
			mac.validate(value)
		except Concern:
			pass
		else:
			assert False, "Failed to raise a Concern: " + repr(value)
	
	def test_mac_pass(self):
		for value in self.good:
			yield self._do_success, value
	
	def test_mac_fail(self):
		for value in self.bad:
			yield self._do_failure, value
	


class TestURLs(object):
	# These URLs borrowed from http://mathiasbynens.be/demo/url-regex
	good = [
			'http://foo.com/blah_blah',
			'http://foo.com/blah_blah/',
			'http://foo.com/blah_blah_(wikipedia)',
			'http://foo.com/blah_blah_(wikipedia)_(again)',
			'http://www.example.com/wpstyle/?p=364',
			'https://www.example.com/foo/?bar=baz&inga=42&quux',
			'http://✪df.ws/123',
			'http://userid:password@example.com:8080',
			'http://userid:password@example.com:8080/',
			'http://userid@example.com',
			'http://userid@example.com/',
			'http://userid@example.com:8080',
			'http://userid@example.com:8080/',
			'http://userid:password@example.com',
			'http://userid:password@example.com/',
			'http://142.42.1.1/',
			'http://142.42.1.1:8080/',
			'http://➡.ws/䨹',
			'http://⌘.ws',
			'http://⌘.ws/',
			'http://foo.com/blah_(wikipedia)#cite-1',
			'http://foo.com/blah_(wikipedia)_blah#cite-1',
			'http://foo.com/unicode_(✪)_in_parens',
			'http://foo.com/(something)?after=parens',
			'http://☺.damowmow.com/',
			'http://code.google.com/events/#&product=browser',
			'http://j.mp',
			'ftp://foo.bar/baz',
			'http://foo.bar/?q=Test%20URL-encoded%20stuff',
			'http://例子.测试',
			'http://उदाहरण.परीक्षा',
			'http://-.~_!$&\'()*+,;=:%40:80%2f::::::@example.com',
			'http://1337.net',
			'http://a.b-c.de',
			'http://223.255.255.254',
			'ftps://foo.bar/',
			'http://a.b--c.de/',
			'http://www.foo.bar./',
			'http://10.1.1.1',
			'http://10.1.1.254',
			'foo.com',
			'rdar://1234',
			'h://test',
			'hTtP://www.pumps.com/',
			'HTTPS://wWw.YAHOO.cO.UK/one/two/three?a=a&b=b&m=m%26m#fragment',
			'sup://192.168.1.102:8080///one//a%20b////?s=kwl%20string#frag',
			'''sup://example.com/:@-._~!$&'()*+,=;:@-._~!$&'()*+,=:@-._~!$&'()*+''',
			'http://[2001:db8:85a3:8d3:1319:8a2e:370:7348]/',
			'undefined://www.pumps.com:9000/',
		]
	
	bad = [
		]
	
	def _do_success(self, value):
		assert uri.validate(value) == value
	
	def _do_failure(self, value):
		try:
			uri.validate(value)
		except Concern:
			pass
		else:
			assert False, "Failed to raise a Concern: " + repr(value)
	
	def test_uris_pass(self):
		for value in self.good:
			yield self._do_success, value
	
	def test_uris_fail(self):
		for value in self.bad:
			yield self._do_failure, value
	

"""

Future failures for http-specific validation.

			'http://',
			'http://.',
			'http://..',
			'http://../',
			'http://?',
			'http://??',
			'http://??/',
			'http://#',
			'http://##',
			'http://##/',
			'http://foo.bar?q=Spaces should be encoded',
			'ftps://foo.bar/',
			'http://a.b--c.de/',
			'http://www.foo.bar./',
			'http://10.1.1.1',
			'http://10.1.1.254',
			'foo.com',
			'rdar://1234',
			'h://test',
			'http:///a',
			'http:// shouldfail.com',
			':// should fail',
			'http://foo.bar/foo(bar)baz quux',
			'http://-error-.invalid/',
			'http://-a.b.co',
			'http://a.b-.co',
			'http://0.0.0.0',
			'http://10.1.1.0',
			'http://10.1.1.255',
			'http://224.1.1.1',
			'http://1.1.1.1.1',
			'http://123.123.123',
			'http://3628126748',
			'http://.www.foo.bar/',
			'http://.www.foo.bar./',
			'//',
			'//a',
			'///a',
			'///',

"""