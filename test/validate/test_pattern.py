from functools import partial
from random import choice, randrange
from string import ascii_letters as letters, digits, punctuation, whitespace

from marrow.schema.testing import ValidationTest
from marrow.schema.validate.pattern import alphanumeric, username, twitterusername, facebookusername, creditcard, hexcolor, alphahexcolor, isbn, slug, uuid


def rs(size=6, chars=letters + digits):
	if isinstance(size, tuple):
		size = randrange(*size)
	return ''.join(choice(chars) for _ in range(size))

bs = partial(rs, chars=punctuation + whitespace)


class TestAlphanumeric(ValidationTest):
	validator = alphanumeric.validate
	valid = (None, ) + tuple(rs((2,11)) for _ in range(10))
	invalid = (bs((5,11)) for _ in range(10))


class TestUsername(ValidationTest):
	validator = username.validate
	valid = ()
	invalid = ()


class TestTwitterUsername(ValidationTest):
	validator = twitterusername.validate
	valid = ()
	invalid = ()


class TestFacebookUsername(ValidationTest):
	validator = facebookusername.validate
	valid = ()
	invalid = ()


class TestCreditCard(ValidationTest):
	validator = creditcard.validate
	valid = (
			'378282246310005',  # Amex
			'371449635398431',  # Amex
			'378734493671000',  # Amex Corporate
			'5610591081018250',  # Australian BankCard
			'30569309025904',  # Diners Club
			'38520000023237',  # Diners Club
			'6011111111111117',  # Discover
			'6011000990139424',  # Discover
			'3530111333300000',  # JCB
			'3566002020360505',  # JCB
			'5555555555554444',  # MC
			'5105105105105100',  # MC
			'5200828282828210',  # MC (Debit)
			'5105105105105100',  # MC (Prepaid)
			'4111111111111111',  # Visa
			'4012888888881881',  # Visa
			'4222222222222',  # Visa
			'4242424242424242',  # Visa
			'4000056655665556',  # Visa (Debit)
		)
	invalid = ('123456')


class TestHexColor(ValidationTest):
	validator = hexcolor.validate
	valid = ('#123', '#112233', '123', '112233', 'def', 'abcdef')
	invalid = ('12', '1234', 'xxyyzz', 'rrggbb')


class TestAlphaHexColor(ValidationTest):
	validator = alphahexcolor.validate
	valid = ('#1234', '#11223344', '1234', '11223344', 'cdef', 'aabbccdd')
	invalid = ('12', '123', '12345', '1122334455', '112233', 'wxyz', 'wwxxyyzz', 'rrggbbaa')


class TestISBN(ValidationTest):
	validator = isbn.validate
	valid = ('9781060394363', '0060394366', '9780306452239')
	invalid = ('978-0060394363', '006039436')


class TestSlug(ValidationTest):
	validator = slug.validate
	valid = ('valid', 'valid-slug', 'evenMoreValid', 'super_valid', '200-may-validate')
	invalid = ('##notevenclose##', )


class TestUUID(ValidationTest):
	validator = uuid.validate
	valid = (
			'00000000-0000-0000-0000-000000000000',
			'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA',
			'ffffffff-ffff-ffff-ffff-ffffffffffff',
			'00010203-0405-0607-0809-0a0b0c0d0e0f',
			'02d9e6d5-9467-382e-8f9b-9300a64ac3cd',
			'12345678-1234-5678-1234-567812345678',
			'6ba7b810-9dad-11d1-80b4-00c04fd430c8',
			
			# Version 3
			'6fa459ea-ee8a-3ca4-894e-db77e160355e',  # DNS: python.org
			'9fe8e8c4-aaa8-32a9-a55c-4535a88b748d',  # URL: http://python.org/
			'658d3002-db6b-3040-a1d1-8ddd7d189a4d',  # X500: c=ca
			
			# Version 5
			'1447fa61-5277-5fef-a9b3-fbc6e44f4af3',  # OID: 1.3.6.1
		)
	invalid = (
			'0', 'aaa',
			'1234567812345678123456781234567',
			'123456781234567812345678123456789',
			'123456781234567812345678z2345678',
			'gggggggg-gggg-gggg-gggg-gggggggggggg',
			
		)
