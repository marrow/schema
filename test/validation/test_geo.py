# encoding: utf-8

from marrow.schema.validation.geo import *


good = [
		(50.010487, -110.114964),  # Clay Face
		(45.123767, -123.113802),  # Firefox Crop Circle
		(27.980070, 86.921377),  # Everest
		(-17.924373, 25.855776)  # Victoria Falls
	]

bad = [
		(-92, 219),
		(103, -540)
	]



def _raises(validator, value):
	try:
		validator.validate(value)
	except Concern:
		pass
	else:
		assert False, "Failed to raise a Concern."


def test_latitude():
	for l, _ in good:
		assert latitude.validate(l) == l
	
	for l, _ in bad:
		_raises(latitude, l)


def test_longitude():
	for _, l in good:
		assert longitude.validate(l) == l
	
	for _, l in bad:
		_raises(longitude, l)


def test_position():
	for p in good:
		assert position.validate(p) == p
	
	for p in bad:
		_raises(position, p)
