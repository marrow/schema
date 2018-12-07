from re import compile, U, I

from . import Pattern


class Alphanumeric(Pattern):
	"""Validate strings only containing letters and numbers, upper- and lower-case."""
	pattern = compile(r'^[a-zA-Z0-9]*$', U | I)

alphanumeric = Alphanumeric()


class Username(Pattern):
	"""A reasonable pattern for username restriction."""
	pattern = compile(r'^[a-z][a-z0-9-_\.]+$', U | I)

username = Username()


class TwitterUsername(Pattern):
	"""Allowable (modern) Twitter usernames."""
	pattern = compile(r'^[a-z0-9_]{1,32}$', U | I)

twitterusername = TwitterUsername()


class FacebookUsername(Pattern):
	"""Allowable Facebook usernames."""
	pattern = compile(r'^[a-z0-9\.]{5,}$', U)

facebookusername = FacebookUsername()


class CreditCard(Pattern):
	"""Basic CreditCard pre-filter."""
	pattern = compile(r'^[0-9]{13,16}$')

creditcard = CreditCard()


class HexColor(Pattern):
	"""An optionally hash-prefixed 6- or 3-digit hex RGB color code."""
	pattern = compile(r'^#?([a-f0-9]{6}|[a-f0-9]{3})$', I)

hexcolor = HexColor()


class AlphaHexColor(Pattern):
	"""An optionally hash-prefixed 8- or 4-digit hex RGBA color code."""
	pattern = compile(r'^#?([a-f0-9]{8}|[a-f0-9]{4})$', I)

alphahexcolor = AlphaHexColor()


class ISBN(Pattern):
	"""A publication ISBN code."""
	pattern = compile(r'(?:(?=.{17}$)97[89][ -](?:[0-9]+[ -]){2}[0-9]+[ -][0-9]|97[89][0-9]{10}|(?=.{13}$)(?:[0-9]+[ -]){2}[0-9]+[ -][0-9Xx]|[0-9]{9}[0-9Xx])')

isbn = ISBN()


class Slug(Pattern):
	"""Generally acceptable URL components for a single URI path element."""
	pattern = compile(r'^[\w_-]+$', U)

slug = Slug()


class UUID(Pattern):
	"""A structurally sound UUID."""
	pattern = compile(r'[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}', I)

uuid = UUID()
