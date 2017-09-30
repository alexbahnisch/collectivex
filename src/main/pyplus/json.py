from collections import OrderedDict as _OrderedDict
from copy import deepcopy as _deepcopy
from json import dump as _dump, dumps as _dumps, load as _load, loads as _loads

from . import common as _common
from .parse import create_lazy_parser
from .path import LazyPath as _LazyPath
from .string import alias2keys as _alias2keys


class _JsonMixin(object):
    def serialize(self, indent=2, sort_keys=True):
        return _dumps(self, indent=indent, sort_keys=sort_keys)

    def to_file(self, path, indent=2, sort_keys=True):
        with _LazyPath(str(path)).write() as tmp_file:
            _dump(self, tmp_file, indent=indent, sort_keys=sort_keys)


class Array(list, _JsonMixin):
    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)(_deepcopy(item) for item in self)

    def __eq__(self, other):
        if isinstance(other, list) and len(self) == len(other):
            for index, item in enumerate(self):
                if item != other[index]:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        if _common.isintlike(index) and 0 <= int(index) < self.length:
            return super(Array, self).__getitem__(int(index))
        else:
            return None

    def __setitem__(self, index, value):
        if _common.isintlike(index) and 0 <= int(index) < self.length:
            super(Array, self).__setitem__(int(index), value)
        elif _common.isintlike(index) and int(index) == self.length:
            self.append(value)
        elif _common.isintlike(index) and int(index) > self.length:
            self.extend([None] * (int(index) - self.length) + [value])

    @property
    def length(self):
        return len(self)

    def concat(self, items):
        if _common.isiterable(items):
            rarg = self.copy()
            rarg.extend(items)
            return rarg
        else:
            rarg = self.copy()
            rarg.append(items)
            return rarg

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def push(self, *items):
        self.extend(items)
        return self.length


# noinspection PyMethodOverriding
class Object(_OrderedDict, _JsonMixin):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("json expected at most 1 arguments, got %s" % len(args))

        if len(args) > 0 and isinstance(args[0], dict):
            for key, value in args[0].items():
                if str(key) not in kwargs:
                    kwargs[str(key)] = value

        elif len(args) > 0 and hasattr(args[0], "__iter__"):
            for inx, items in enumerate(args[0]):
                if _common.ispair(items):
                    if str(items[0]) not in kwargs:
                        kwargs[str(items[0])] = items[1]
                elif _common.issequence(items) and len(items) > 2:
                    raise ValueError("json update sequence element #%s has length %s; 2 is required" % inx, len(items))
                else:
                    raise TypeError("cannot convert json update sequence element #%s to a sequence" % inx)

        elif len(args) > 0:
            raise TypeError("'%s' object is not iterable" % type(args[0]).__name__)

        super(Object, self).__init__(kwargs)

    def __contains__(self, key):
        return super(Object, self).__contains__(str(key))

    def __copy__(self):
        return type(self)(self)

    def __deepcopy__(self, memo):
        return type(self)({key: _deepcopy(value) for key, value in self.items()})

    def __eq__(self, other):
        if isinstance(other, dict) and self.keys() == other.keys():
            for key, value in other.items():
                if self[key] != value:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, key):
        return self.__getitem__(str(key))

    def __getitem__(self, key):
        return super(Object, self).get(str(key))

    def __repr__(self):
        return dict.__repr__(self)

    def __setattr__(self, key, value):
        self.__setitem__(str(key), value)

    def __setitem__(self, key, value):
        return super(Object, self).__setitem__(str(key), value)

    def assign(self, *others):
        assert all(isinstance(other, type(self)) for other in others)
        for other in others:
            for keys, values in other.items():
                self[keys] = values

        return self

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__({})

    def items(self, parser=False):
        if parser is False:
            return super().items()
        else:
            parser = create_lazy_parser(parser)
            return [(parser(key), value) for key, value in super().items()]

            # TODO - add merge


class JSON(object):
    __ARRAY__ = Array
    __OBJECT__ = Object

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls.__OBJECT__({key: cls.from_object(value) for key, value in dict_.items()})

    @classmethod
    def from_file(cls, path, alias=None, errors=True):
        path, alias = _LazyPath(path), _alias2keys(alias) if alias is not None else []

        if path.exists():
            with path.read() as tmp_file:
                rarg = cls.from_object(_load(tmp_file))

                for key in alias:
                    rarg = rarg[key]
                    if rarg is None:
                        return None

                return rarg

        else:
            if bool(errors):
                raise FileNotFoundError("[Errno 2] No such file or directory: '{}'".format(path))
            else:
                return None

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, list)
        return cls.__ARRAY__(cls.from_object(item) for item in list_)

    @classmethod
    def from_object(cls, obj):
        if isinstance(obj, dict):
            return cls.from_dict(obj)
        elif isinstance(obj, list):
            return cls.from_list(obj)
        else:
            return obj

    @classmethod
    def parse(cls, string, errors=False):
        try:
            rarg = _loads(str(string))
            if isinstance(rarg, dict):
                return cls.from_dict(rarg)
            elif isinstance(rarg, list):
                return cls.from_list(rarg)

        except ValueError as error:
            if bool(errors):
                raise error
            else:
                return string
