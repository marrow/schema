import sys
import copy

from logging import getLevelName, DEBUG, INFO, WARNING, ERROR, CRITICAL


class Concern(Exception):
	"""There was an error validating data.
	
	Only `logging.ERROR` (and above) validation concerns should be treated as actual errors.
	"""
	
	def __init__(self, level=ERROR, message="Unspecified error.", *args, **kw):
		"""Can be instantiated with the message first (and no way to populate a level other than ERROR)."""
		
		if isinstance(level, int):
			args = (level, message) + args
		else:
			args = (message, ) + args
			message = level
			level = ERROR
		
		self.message = message
		self.level = level
		self.concerns = kw.pop('concerns', [])
		self.kwargs = kw
		
		super().__init__(*args)
	
	def __str__(self):
		"""Format the validation concern for human consumption.
		
		We have the seemingly pointless wrapping call to str() here to allow for lazy translation.
		"""
		return str(self.message).format(*self.args, **self.kwargs)
	
	def __repr__(self):
		result = '{0}({1}, "{2}")'.format(
				self.__class__.__name__,
				getLevelName(self.level),
				str(self).replace('"', '\"')
			)
		
		return result
