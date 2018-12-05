import pytest
import warnings

from marrow.schema.declarative import BaseAttribute, BaseDataAttribute
from marrow.schema.util import DeclarativeAttributes


DEPRECATED = (
		(BaseAttribute, 'Container'),
		(BaseDataAttribute, 'DataAttribute'),
		(DeclarativeAttributes, 'Attributes')
	)


@pytest.mark.parametrize("cls,dst", DEPRECATED)
def test_deprecation(cls, dst):
	with warnings.catch_warnings(record=True) as w:
		warnings.simplefilter('always')
		
		cls()
		
		assert len(w) == 1, "Only one warning should be raised."
		assert issubclass(w[-1].category, DeprecationWarning), "Warning must be a DeprecationWarning."
		assert dst in str(w[-1].message), "Warning should mention correct class to use."


def test_depreciated_validation_import():
	with warnings.catch_warnings(record=True) as w:
		warnings.simplefilter('always')
		
		import marrow.schema.validation
		import marrow.schema.validation.base
		import marrow.schema.validation.compound
		import marrow.schema.validation.date
		import marrow.schema.validation.geo
		import marrow.schema.validation.network
		import marrow.schema.validation.pattern
		import marrow.schema.validation.testing
		import marrow.schema.validation.util
		
		assert len(w) == 1, "Only one warning should be raised."
		assert issubclass(w[-1].category, DeprecationWarning), "Warning must be DeprecationWarning."
		assert 'marrow.schema.validate' in str(w[-1].message), "Warning should mention correct module to import."
