# encoding: utf-8

from __future__ import unicode_literals

import re
import sys
import uuid
import datetime

from .. import Attributes
from .base import Concern, Validator, Pattern


if sys.version_info > (3, ):
	unicode = str
	str = bytes



"""

Alpha-Numeric "[a-zA-Z0-9{extra}]+"
Username "^[a-zA-Z][a-zA-Z0-9-_\.]+$
TwitterUsername "^[A-Za-z0-9_]{1,32}$"
FacebookUsername "^[a-z\d\.]{5,}$"

CreditCard "[0-9]{13,16}"

HexColor "^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"
HexAlphaColor "^#?([a-fA-F0-9]{8}|[a-fA-F0-9]{4})$"

ISBN "(?:(?=.{17}$)97[89][ -](?:[0-9]+[ -]){2}[0-9]+[ -][0-9]|97[89][0-9]{10}|(?=.{13}$)(?:[0-9]+[ -]){2}[0-9]+[ -][0-9Xx]|[0-9]{9}[0-9Xx])"

TwitterCharacterCount
	url compression
	combine diacritical marks
	number of codepoints in NFC normalized text
	
	from unicodedata import normalize
	length = len(normalize("NFC", value))

"""





class SlugValidator(Pattern):
	pattern = re.compile(r'^[-\w]+$')


class URLValidator(Pattern):
	# This is a terrible pattern, and a terrible way to go about doing this.
	
	pattern = re.compile(
			r'^(?:http|ftp)s?://'  # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
			r'localhost|'  # localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
			r'(?::\d+)?'  # optional port
			r'(?:/?|[/?]\S+)$',
			re.IGNORECASE
		)


class EmailValidator(Pattern):
	# Same here.  Ugh.
	
	pattern = re.compile(
			r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
			r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
			r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,253}[A-Z0-9])?\.)+[A-Z]{2,6}$',
			re.IGNORECASE  # domain
		)


class UUIDValidator(Validator):
	def __call__(self, value):
		super(UUIDValidator, self)(value)
		
		if isinstance(value, uuid.UUID):
			return
		
		try:
			value = uuid.UUID(value)
		except:
			raise Concern(logging.CRITICAL, "Value is not a valid UUID.")
