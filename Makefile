PROJECT = marrow.schema
USE = development

.PHONY: all develop clean veryclean test release

all: clean develop test

develop: ${PROJECT}.egg-info/PKG-INFO

clean:
	find . -name __pycache__ -exec rm -rfv {} +
	find . -iname \*.pyc -exec rm -fv {} +
	find . -iname \*.pyo -exec rm -fv {} +
	rm -rvf build htmlcov

veryclean: clean
	rm -rvf *.egg-info .packaging

test: develop
	./setup.py test

release:
	./setup.py sdist bdist_wheel ${RELEASE_OPTIONS}
	open .packaging

${PROJECT}.egg-info/PKG-INFO: setup.py setup.cfg marrow/schema/release.py
	@mkdir -p ${VIRTUAL_ENV}/lib/pip-cache
	pip install --cache-dir "${VIRTUAL_ENV}/lib/pip-cache" -e ".[${USE}]"
