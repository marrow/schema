# encoding: utf-8

from collections import Sequence
from numbers import Number

from .base import Validator, Length, Range, Instance
from .compound import All
from .exc import Concern


class Latitude(All):
	validators = [
			Instance(Number),
			Range(-90, 90)
		]

latitude = Latitude()


class Longitude(All):
	validators = [
			Instance(Number),
			Range(-180, 180)
		]

longitude = Longitude()


class Position(All):
	validators = [
			Instance(Sequence),
			Length(slice(2, 3))  # exactly two elements long
		]
	
	def validate(self, value, context=None):
		value = super(Position, self).validate(value, context)
		
		_lat, _long = value
		
		latitude.validate(_lat)
		longitude.validate(_long)
		
		return value

position = Position()
