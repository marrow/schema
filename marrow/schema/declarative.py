# encoding: utf-8

from __future__ import unicode_literals

from marrow.util.object import NoDefault
from marrow.schema.meta import Element


class BaseAttribute(Element):
    def __init__(self, *args, **kw):
        super(BaseAttribute, self).__init__()
        arguments = self.__process_arguments(args, kw)
        
        self.__data__ = dict()
        
        for name, value in arguments.iteritems():
            setattr(self, name, value)
    
    def __process_arguments(self, args, kw):
        if len(args) > len(self.__attributes__):
            raise TypeError('{0} takes no more than {1} argument{2} ({3} given)'.format(
                    self.__class__.__name__,
                    len(self.__attributes__),
                    '' if len(self.__attributes__) == 1 else 's',
                    len(args)
                ))
        
        names = [name for name in self.__attributes__.keys() if not name[0] == '_'][:len(args)]
        duplicates = set(names).intersection(kw.iterkeys())
        
        if duplicates:
            raise TypeError('{0} got multiple values for keyword argument{1}: {2}'.format(
                    self.__class__.__name__,
                    '' if len(duplicates) == 1 else 's',
                    ', '.join(duplicates)
                ))
        
        return dict(kw, **{names[i]: arg for i, arg in enumerate(args)})


class BaseDataAttribute(BaseAttribute):
    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        
        try:
            return obj.__data__[self.__name__]
        except KeyError:
            raise AttributeError('\'{0}\' object has no attribute \'{1}\''.format(
                    obj.__class__.__name__,
                    self.__name__
                ))
    
    def __set__(self, obj, value):
        obj.__data__[self.__name__] = value
    
    def __delete__(self, obj):
        del obj.__data__[self.__name__]


class Attribute(BaseDataAttribute):
    """An attribute whose instance value is stored within the containing object.
    
    All "data" is stored in the instance's __data__ dictionary.  The key defaults
    to the DataAttribute's instance name and can be overridden by passing a name
    as the first positional parameter, or as a keyword argument.
    
    If assign is True if the default value is ever utilized, immediately pretend
    the default value was assigned to this attribute.
    """
    
    name = BaseDataAttribute()
    default = BaseDataAttribute()
    assign = False  # If the value is missing, do we outright create it?
    
    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        
        try:
            name = self.name
        except AttributeError:
            name = self.__name__
        
        try:
            value = obj.__data__[name]
        except KeyError:
            value = NoDefault
        
        # Attempt to utilize the defined default value.
        if value is NoDefault:
            try:
                default = self.default
            except AttributeError:
                pass
            else:
                value = default() if callable(default) else default
                if self.assign:
                    self.__set__(obj, value)
        
        # If we still don't have a value, this attribute doesn't yet exist.
        if value is NoDefault:
            raise AttributeError('\'{0}\' object has no attribute \'{1}\''.format(
                    obj.__class__.__name__,
                    self.__name__
                ))
        
        return value
    
    def __set__(self, obj, value):
        try:
            name = self.name
        except AttributeError:
            name = self.__name__
        
        obj.__data__[name] = value
    
    def __delete__(self, obj):
        try:
            name = self.name
        except AttributeError:
            name = self.__name__
        
        del obj.__data__[name]
