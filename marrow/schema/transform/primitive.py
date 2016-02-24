# encoding: utf-8

raise ImportError("For future use.")

from __future__ import unicode_literals

from ..compat import unicode
from .base import Concern, Transform, Attribute


class Primitive(Transform):
	pass




"""

Primitive

VInteger (min/max)
VFloat (min/max)

Decimal (min/max)
Complex

String
Binary
Unicode

Null

Tuple
List
Set



Mapping
Sequence
Tuple
Integer
Float
String
Decimal
Boolean
DateTime
Date
Time

"""