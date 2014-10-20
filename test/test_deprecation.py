# encoding: utf-8

import pytest
import warnings

from marrow.schema.compat import unicode
from marrow.schema.declarative import BaseAttribute, BaseDataAttribute


class TestDeprecatedClasses:
	def test_base_attribute(self):
		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter('always')
			
			BaseAttribute()
			
			assert len(w) == 1, "Only one warning should be raised."
			assert issubclass(w[-1].category, DeprecationWarning), "Warning must be a DeprecationWarning."
			assert "Container" in unicode(w[-1].message), "Warning should mention correct class to use."
	
	def test_base_data_attribute(self):
		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter('always')
			
			BaseDataAttribute()
			
			assert len(w) == 1, "Only one warning should be raised."
			assert issubclass(w[-1].category, DeprecationWarning), "Warning must be a DeprecationWarning."
			assert "DataAttribute" in unicode(w[-1].message), "Warning should mention correct class to use."
