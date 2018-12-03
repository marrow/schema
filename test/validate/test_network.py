from marrow.schema.testing import ValidationTest
from marrow.schema.validate.network import ipv4, ipv6, ipaddress, cidrv4, cidrv6, cidr, hostname, dnsname, mac, uri


class TestIPv4(ValidationTest):
	validator = ipv4.validate
	
	valid = (
			'1.1.1.1',
			'255.255.255.255',
			'192.168.1.1',
			'10.10.1.1',
			'132.254.111.10',
			'26.10.2.10',
			'127.0.0.1'
		)
	
	invalid = (
			'10.10.10',
			'10.10',
			'10',
			'a.a.a.a',
			'10.0.0.a',
			'10.10.10.256',
			'222.222.2.999',
			'999.10.10.20',
			'2222.22.22.22',
			'22.2222.22.2'
		)


class TestIPv6(ValidationTest):
	validator = ipv6.validate
	
	valid = (
			'2000::',  # Incomplete address, technically valid.
			'2002:c0a8:101::42',  # Invalid range, technically valid.
			'2003:dead:beef:4dad:23:46:bb:101',
			'::192:168:0:1',  # Invalid IPv4 literal, technically valid.
			'::ffff:192.168.0.1',  # Actually valid IPv4 literal.
			'2001:3452:4952:2837::',
			'::',
			'2001::ce49:7601:e866:efff:62c3:fffe',  # Teredo tunnel.
			'0001:0002:0003:0004:0005:0006:0007:0008',  # Long form.
			'2608::3:5',  # Compact form.
			'ff02::1:2',  # Multicast.
			'2001:4860:4001:803::1011',  # Google.
		)
	
	invalid = (
			'wxyz:',  # Not even close.
			# '2003:dead:beef:cafe:babe:8bad:f00d:b0da:face:d00d',  # Too long, doesn't fail?
		)


class TestIPAddress(ValidationTest):
	validator = ipaddress.validate
	valid = TestIPv4.valid + TestIPv6.valid
	invalid = TestIPv4.invalid + TestIPv6.invalid


class TestCIDRv4(ValidationTest):
	validator = cidrv4.validate
	valid = ('10.0.0.0/8', '172.16.0.0/12', '196.168.0.0/16', '192.168.1.100/24')
	invalid = ('10/8', '8.8.8.8/33')


class TestCIDRv6(ValidationTest):
	validator = cidrv6.validate
	valid = ('2620:0:2d0:2da:0:0:0:0/63', 'abcd:ef01::/64')
	invalid = ('dead:face::/129', )


class TestCIDR(ValidationTest):
	validator = cidr.validate
	valid = TestCIDRv4.valid + TestCIDRv6.valid
	invalid = TestCIDRv4.invalid + TestCIDRv6.invalid


class TestHostname(ValidationTest):
	validator = hostname.validate
	
	valid = (
			'google.com',
			'itsnotmygoddamnplanetunderstandmonkeyboy.wpi.edu',
			'a' * 63 + '.' + 'b' * 63,
			'xn--eckwd4c7c.xn--zckzah',
			'xn--bcher-kva.ch',
			'xn--zckzah.xn--zckzah',
			'yahoo.com',
			'facebook.com',
			'google.to.cc',
			'mkyong-info.com',
			'mkyong.com.au',
			'verdi.com.my',
			'google.t.co',
			'google.t.t.co',
			'abc.99.com',
			'abc.mkyong-info.com',
			'abc-123.mkyong-99b.com.my',
			'mkyong',
		)
	
	invalid = (
			'a' * 64 + '.' + 'b' * 63,
			'123,345.com',
			'.com.my',
			'%*.com',
			'gmail.a',
			'youtube.com/users/abc',
			'google.t.t.t',
			'mkyong.com.abcdefg123',
		)


class TestDNSName(ValidationTest):
	validator = dnsname.validate
	valid = TestHostname.valid + ('tenthdimension.wpi.edu.', )
	invalid = TestHostname.invalid + ()


class TestMACs(ValidationTest):
	validator = mac.validate
	valid = ('3D:F2:C9:A6:B3:4F', '3d:f2:c9:a6:b3:4f', '3D-F2-C9-A6-B3-4F')
	invalid = ('3D:F2:AC9:A6:B3:4F', '3D:F2:C9:A6:B3:4F:00', ':F2:C9:A6:B3:4F', 'F2:C9:A6:B3:4F', '3D-F2:C9-A6:B3-4F')


class TestURLs(ValidationTest):
	validator = uri.validate
	
	# These URLs borrowed from http://mathiasbynens.be/demo/url-regex
	valid = (
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
		)
	
	invalid = ()
	

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
