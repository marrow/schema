from marrow.schema.testing import ValidationTest
from marrow.schema.validate.geo import latitude, longitude, position


class TestGeographicLatitude(ValidationTest):
	validator = latitude.validate
	valid = (45, -45, 90, -90, 0)
	invalid = (110, 360, 420, -960)


class TestGeographicLongitude(ValidationTest):
	validator = longitude.validate
	valid = TestGeographicLatitude.valid + (110, -110, -180, 180)
	invalid = TestGeographicLatitude.invalid[1:]


class TestGeographicPosition(ValidationTest):
	validator = position.validate
	
	valid = (
			(50.010487, -110.114964),  # Clay Face
			(45.123767, -123.113802),  # Firefox Crop Circle
			(27.980070, 86.921377),  # Everest
			(-17.924373, 25.855776)  # Victoria Falls
		)
	
	invalid = (
			(-92, 219),
			(103, -540)
		)
