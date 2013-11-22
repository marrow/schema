# encoding: utf-8

from __future__ import unicode_literals

from collections import OrderedDict
from marrow.schema.declarative import BaseAttribute, Attribute


class DeclarativeAttributes(BaseAttribute):
    only = Attribute(default=None)
    
    def __get__(self, obj, cls=None):
        if not obj:
            obj = cls
        
        if not self.only:
            return obj.__attributes__.iteritems()
        
        return OrderedDict((k, v) for k, v in obj.__attributes__.iteritems() if isinstance(v, self.only))
