# encoding: utf-8

import sys

if sys.version_info > (3, ):  # pragma: no cover
	unicode = str
	str = bytes
else:  # pragma: no cover
	range = xrange

try:  # pragma: no cover
	from collections import OrderedDict as odict
except ImportError:  # pragma: no cover
	from ordereddict import OrderedDict as odict
