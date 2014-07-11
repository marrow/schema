# encoding: utf-8

from __future__ import unicode_literals

from re import compile, U, I

from .base import Pattern


class Alphanumeric(Pattern):
	pattern = compile(r'[0-Z]+$', U | I)


class Username(Pattern):
	pattern = compile(r'^[a-z][a-z0-9-_\.]+$', U | I)


class TwitterUsername(Pattern):
	pattern = compile(r'^[a-z0-9_]{1,32}$', U | I)


class FacebookUsername(Pattern):
	pattern = compile(r'^[a-z0-9\.]{5,}$', U)


class CreditCard(Pattern):
	pattern = compile(r'^[0-9]{13,16}$')


class HexColor(Pattern):
	pattern = compile(r'^#?([a-f0-9]{6}|[a-f0-9]{3})$', I)


class ISBN(Pattern):
	pattern = compile(r'(?:(?=.{17}$)97[89][ -](?:[0-9]+[ -]){2}[0-9]+[ -][0-9]|97[89][0-9]{10}|(?=.{13}$)(?:[0-9]+[ -]){2}[0-9]+[ -][0-9Xx]|[0-9]{9}[0-9Xx])')


class Slug(Pattern):
	pattern = compile(r'^[\w-]+$', U)


class UUID(Pattern):
	pattern = compile(r'[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}', I)
