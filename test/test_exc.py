from marrow.schema.exc import Concern, WARNING, ERROR, CRITICAL


def test_basic_concern_text():
	concern = Concern("This is a sample failure.")
	assert str(concern) == "This is a sample failure."


def test_basic_concern_text_replacement():
	concern = Concern("{who} has failed me for the {times} time.", who="Bob Dole", times="last")
	assert str(concern) == "Bob Dole has failed me for the last time."


def test_basic_concern_positional_replacement():
	concern = Concern("{0} has failed me for the {1} time.", "Bob Dole", "last")
	assert str(concern) == "Bob Dole has failed me for the last time."


def test_concern_level():
	concern = Concern(CRITICAL, "This is a sample catastrophic failure.")
	assert concern.level == CRITICAL
	assert str(concern) == "This is a sample catastrophic failure."
	assert repr(concern) == 'Concern(CRITICAL, "This is a sample catastrophic failure.")'
	
	concern = Concern(WARNING, "This is a sample warning.")
	assert concern.level == WARNING
	assert str(concern) == "This is a sample warning."
	assert repr(concern) == 'Concern(WARNING, "This is a sample warning.")'


def test_basic_concern_repr():
	concern = Concern("This is a sample failure.")
	assert repr(concern) == 'Concern(ERROR, "This is a sample failure.")'
	
	concern = Concern("{who} has failed me for the {times} time.", who="Bob Dole", times="last")
	assert repr(concern) == 'Concern(ERROR, "Bob Dole has failed me for the last time.")'
	
	concern = Concern("{0} has failed me for the {1} time.", "Bob Dole", "last")
	assert repr(concern) == 'Concern(ERROR, "Bob Dole has failed me for the last time.")'


def test_nested_concern():
	child = Concern("Oh noes.")
	concern = Concern("Uh-oh.", concerns=[child])
	
	assert concern.concerns == [child]
