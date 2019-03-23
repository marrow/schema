#!/usr/bin/env python3

from setuptools import setup
from sys import argv, version_info as python_version
from pathlib import Path


if python_version < (3, 5):
	raise SystemExit("Python 3.5 or later is required.")

here = Path(__file__).resolve().parent
exec((here / "marrow" / "schema" / "release.py").read_text('utf-8'))

tests_require = ['pytest', 'pytest-cov', 'pytest-flakes', 'pytest-isort']


setup(
	name = "marrow.schema",
	version = version,
	
	description = description,
	long_description = (here / 'README.rst').read_text('utf-8'),
	url = url,
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = ('declarative syntax', 'metaprogramming', 'schema toolkit'),
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3.7",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = ('marrow.schema', ),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	zip_safe = False,
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(argv) else [],
	
	install_requires = [],
	
	extras_require = dict(
			development = tests_require,
		),
	
	tests_require = tests_require,
)
