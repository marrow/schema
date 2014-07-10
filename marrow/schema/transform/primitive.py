# encoding: utf-8

from __future__ import unicode_literals

import sys
import copy

from logging import ERROR

from .. import Attribute, Attributes
from .base import Concern, Validator


class Primitive(Validator):
	




"""

Primitive

Boolean

VInteger (min/max)
VFloat (min/max)

Decimal (min/max)
Complex

VNumber = any(Integer, Float, Decimal, …)

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