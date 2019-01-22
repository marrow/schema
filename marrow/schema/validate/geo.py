from collections.abc import Sequence
from numbers import Number

from . import Validator, Length, Range, Instance
from .compound import All


class Latitude(All):
	"""Validate the given value as a number between -90 and +90 in decimal degrees, representing latitude."""
	
	validators = [
			Instance(Number),
			Range(-90, 90)
		]

latitude = Latitude()


class Longitude(All):
	"""Validate the given value as a number between -180 and +180 in decimal degrees, representing longitude."""
	validators = [
			Instance(Number),
			Range(-180, 180)
		]

longitude = Longitude()


class Position(All):
	"""Validate the given value as any sequence of exactly two elements representing latitude and longitude."""
	
	validators = [
			Instance(Sequence),
			Length(slice(2, 3))  # exactly two elements long
		]
	
	def validate(self, value, context=None):
		value = super().validate(value, context)
		
		_lat, _long = value
		
		latitude.validate(_lat)
		longitude.validate(_long)
		
		return value

position = Position()
