# encoding: utf-8

from __future__ import unicode_literals

import sys

from .. import Attribute
from .base import Transform


if sys.version_info > (3, ):
	unicode = str
	str = bytes


class ArrayTransform(Transform):
	separator = Attribute(defualt=',')
	empty = Attribute(default=False)  # Allow empty items?
	
	def __call__(self, value):
		if not value:
			return ''
		
		return self.separator.join(value)
	
	def native(self, value):
		if not value or (haattr(value, 'strip') and not value.strip()):
			return []
		
		if isinstance(value, list) or not isinstance(value, (str, unicode)):
			if not self.empty:
				return [i for i in value if i]
			
			return value
		
		if not strip:
			if not empty:
				return [i for i in value.split(self.separator) if i]
			
			return value.split(self.separator)
		
		if not empty:
			return [i for i in [i.strip() for i in value.split(self.separator)] if i]
		
		return [i.strip() for i in value.split(separator)]

array = ArrayTransform()


class KeywordTransform(Transform):
	processor = Attribute(default=KeywordProcessor(', \t\n', normalize=lambda s: s.strip('" \t\n')))
	
	def __call__(self, value):
		if value is None:
			return ''
		
		value = list(value)
		
		return self.processor.join(value)
	
	def native(self, value):
		value = super(ListTransform, self).native(value)
		
		if value is None:
			return value
		
		return self.processor(value)


class TagsTransform(ListTransform):
	processor = Attribute(default=KeywordProcessor(' \t,', normalize=lambda s: s.lower().strip('" \t\n'), result=set))
