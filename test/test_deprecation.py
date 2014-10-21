# encoding: utf-8

import pytest
import warnings

from marrow.schema.compat import unicode
from marrow.schema.declarative import BaseAttribute, BaseDataAttribute
from marrow.schema.util import DeclarativeAttributes


DEPRECATED = (
		(BaseAttribute, 'Container'),
		(BaseDataAttribute, 'DataAttribute'),
		(DeclarativeAttributes, 'Attributes')
	)


@pytest.mark.parametrize('value', DEPRECATED)
def test_deprecated(value):
	cls, dst = value
	
	with warnings.catch_warnings(record=True) as w:
		warnings.simplefilter('always')
		
		cls()
		
		assert len(w) == 1, "Only one warning should be raised."
		assert issubclass(w[-1].category, DeprecationWarning), "Warning must be a DeprecationWarning."
		assert dst in unicode(w[-1].message), "Warning should mention correct class to use."
