# encoding: utf-8

"""Compatibility helpers to bridge the differences between Python 2 and Python 3.

Similar in purpose to [`six`](https://warehouse.python.org/project/six/).
"""

# ## Imports

import sys


# ## Version Detection

py2 = sys.version_info < (3, )
py3 = sys.version_info > (3, )


# ## Builtins Compatibility

if py3:  # pragma: no cover
	native = str
	unicode = str
	str = bytes
else:  # pragma: no cover
	native = str
	unicode = unicode
	str = str
	range = xrange


# ## Ordered Dictionaries

try:  # pragma: no cover
	from collections import OrderedDict as odict
except ImportError:  # pragma: no cover
	from ordereddict import OrderedDict as odict
