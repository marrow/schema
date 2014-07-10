# encoding: utf-8

from __future__ import unicode_literals

import sys
import datetime

from .base import Transform, Attribute


if sys.version_info > (3, ):
	unicode = str
	str = bytes


class DateTimeTransform(Transform):
	base = Attribute(defualt=datetime.datetime)
	format = "%Y-%m-%d %H:%M:%S"
	
	def __call__(self, value):
		if not value:
			return ''
		
		return super(DateTimeTransform, self)(value.strftime(self.format))
	
	def native(self, value):
		value = super(DateTimeTransform, self).native(value)
		
		return self.base.strptime(value, self.format)
