import re
from inspect import isroutine

from .base import Concern, Transform, DataAttribute, Attribute


class TokenPatternAttribute(DataAttribute):
	"""Lazy construction of the regular expression needed for token processing."""
	
	def __get__(self, obj, cls=None):
		# If this is class attribute (and not instance attribute) access, we return ourselves.
		if obj is None:
			return self
		
		# Attempt to retrieve the cached value from the warehouse.
		try:
			return obj.__data__[self.__name__]
		except KeyError:
			pass
		
		# No stored value?  No problem!  Let's calculate it.
		
		separators = obj.separators
		groups = obj.groups
		quotes = obj.quotes
		
		if groups and None not in groups:
			groups = [None] + list(groups)
		
		expression = ''.join((
				# Trap possible leading space or separators.
				('[\s%s]*' % (''.join(separators), )),
				'(',
					# Pass groups=('+','-') to handle optional leading + or -.
					('[%s]%s' % (''.join([i for i in list(groups) if i is not None]), '?' if None in groups else '')) if groups else '',
					# Match any amount of text (that isn't a quote) inside quotes.
					''.join([(r'%s[^%s]+%s|' % (i, i, i)) for i in quotes]) if quotes else '',
					# Match any amount of text that isn't whitespace.
					('[^%s]+' % (''.join(separators), )),
				')',
				# Match possible separator character.
				('[%s]*' % (''.join(separators), )),
			))
		
		value = (expression, re.compile(expression))
		
		self.__set__(obj, value)
		
		return value


class Token(Transform):
	separators = Attribute(default=' \t')
	quotes = Attribute(default="\"'")
	groups = Attribute(default=[])
	group = Attribute(default=None)  # None or 'dict' or some other handler.
	normalize = Attribute(default=None)
	sort = Attribute(default=False)
	cast = Attribute(default=list)
	
	pattern = TokenPatternAttribute()
	
	def native(self, value, context=None):
		value = super().native(value, context)
		
		if value is None:
			return None
		
		pattern, regex = self.pattern
		matches = regex.findall(value)
		
		if isroutine(self.normalize):
			matches = [self.normalize(i) for i in matches]
		
		if self.sort:
			matches.sort()
		
		if not self.groups:
			return self.cast(matches)
		
		groups = dict([(i, list()) for i in self.groups])
		if None not in groups:
			groups[None] = list() # To prevent errors.
		
		for i in matches:
			if i[0] in self.groups:
				groups[i[0]].append(i[1:])
			else:
				groups[None].append(i)
		
		if self.group is dict:
			return groups
		
		if not self.group:
			results = []
			
			for group in self.groups:
				results.extend([(group, match) for match in groups[group]])
			
			return self.cast(results)
		
		return self.group([[match for match in groups[group]] for group in self.groups])
	
	def foreign(self, value, context=None):
		value = super().foreign(value, context)
		
		if value is None:
			return None
		
		def sanatize(keyword):
			if not self.quotes:
				return keyword
			
			for sep in self.separators:
				if sep in keyword:
					return self.quotes[0] + keyword + self.quotes[0]
			
			return keyword
		
		if self.group is dict:
			if not isinstance(value, dict):
				raise Concern("Dictionary grouped values must be passed as a dictionary.")
			
			return self.separators[0].join([((prefix or '') + sanatize(keyword)) for prefix, keywords in sorted(list(value.items())) for keyword in sorted(value[prefix])])
		
		if not isinstance(value, (list, tuple, set)):
			raise Concern("Ungrouped values must be passed as a list, tuple, or set.")
		
		value = [sanatize(keyword) for keyword in value]
		
		return self.separators[0].join(sorted(value) if self.sort else value)


# A lowercase-normalized ungrouped tag set processor, returning only unique tags.
tags = Token(separators=' \t,', normalize=lambda s: s.lower().strip('"'), cast=set)

# A tag search; as per tags but grouped into a dictionary of sets for normal (None), forced inclusion (+) or exclusion (-).
tag_search = Token(separators=' \t,', normalize=lambda s: s.lower().strip('"'), cast=set, groups=['+', '-'], group=dict)

# A search keyword processor which retains quotes and groups into a dictionary of lists; no normalization is applied.
terms = Token(groups=['+', '-'], group=dict)


# VETO: Extract

'''
class DateTimeTransform(Transform):
	base = Attribute(defualt=datetime.datetime)
	format = "%Y-%m-%d %H:%M:%S"
	
	def __call__(self, value):
		if not value:
			return ''
		
		return super()(value.strftime(self.format))
	
	def native(self, value):
		value = super().native(value)
		
		return self.base.strptime(value, self.format)
'''
