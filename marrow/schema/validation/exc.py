# encoding: utf-8

from __future__ import unicode_literals

import sys
import copy

from logging import getLevelName, DEBUG, INFO, WARNING, ERROR, CRITICAL

from ..compat import py3, unicode


class Concern(Exception):
	"""There was an error validating data.
	
	Only `logging.ERROR` (and above) validation concerns should be treated as actual errors.
	"""
	
	def __init__(self, level=ERROR, message="Unspecified error.", *args, **kw):
		"""Can be instantiated with the message first (and no way to populate a level other than ERROR)."""
		
		if not isinstance(level, int):
			args = (message, ) + args
			message = level
			level = ERROR
		
		self.message = message
		self.level = level
		self.concerns = kw.pop('concerns', [])
		self.kwargs = kw
		
		super(Concern, self).__init__(*args)
	
	def __unicode__(self):
		"""Format the validation concern for human consumption.
		
		We have the seemingly pointless wrapping call to unicode() here to allow for lazy translation.
		"""
		return unicode(self.message).format(*self.args, **self.kwargs)
	
	if py3:  # pragma: no cover
		__str__ = __unicode__
		del __unicode__
	
	def __repr__(self):
		result = '{0}({1}, "{2}")'.format(
				self.__class__.__name__,
				getLevelName(self.level),
				unicode(self).replace('"', '\"')
			)
		
		return result
