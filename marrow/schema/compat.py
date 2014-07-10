# encoding: utf-8

import sys

py2 = sys.version_info < (3, )
py3 = sys.version_info > (3, )

if py3:  # pragma: no cover
	unicode = str
	str = bytes
else:  # pragma: no cover
	unicode = unicode
	str = str
	range = xrange

try:  # pragma: no cover
	from collections import OrderedDict as odict
except ImportError:  # pragma: no cover
	from ordereddict import OrderedDict as odict
