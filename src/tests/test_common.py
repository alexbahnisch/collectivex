#!/usr/bin/env python
from decimal import Decimal

from pyplus.common import *
from pyplus.path import LazyPath

DECIMAL = Decimal(1.5)
DICT = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
FLOAT = 1.5
INT = 1
LIST = [1, 2, 3, 4, 5]
MAPPABLE = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
OBJECT = object()
SET = {1, 2, 3, 4, 5}
STRING = "string"
B_STRING = b"string"
U_STRING = u"string"
TUPLE = (1, 2, 3, 4, 5)


class IsIntLike(object):
    def __int__(self):
        return 1


class IsIterable(object):
    def __iter__(self):
        return iter(LIST)


class IsListLike(object):
    def __getitem__(self, item):
        return 1

    def __iter__(self):
        return iter(LIST)

    def __len__(self):
        return 5

    def __setitem__(self, key, value):
        pass


class IsPair(object):
    def __iter__(self):
        return iter([1, 2])

    def __len__(self):
        return 2


class IsMappable(object):
    def __iter__(self):
        return iter([IsPair()])


class IsSequence(object):
    def __iter__(self):
        return iter([1, 2, 3])

    def __len__(self):
        return 3


class IsTupLike(object):
    def __getitem__(self, item):
        return 1

    def __iter__(self):
        return iter(LIST)

    def __len__(self):
        return 5


class NotMappable(object):
    def __iter__(self):
        return iter([IsSequence()])


def test_isintlike():
    assert isintlike("1")
    assert isintlike(False)
    assert isintlike(FLOAT)
    assert isintlike(INT)
    assert isintlike(IsIntLike())


def test_isintlike_not():
    assert not isintlike(None)
    assert not isintlike(OBJECT)
    assert not isintlike(SET)
    assert not isintlike(STRING)
    assert not isintlike(B_STRING)
    assert not isintlike(U_STRING)


def test_isiterable():
    assert isiterable(DICT)
    assert isiterable(IsIterable())
    assert isiterable(LIST)
    assert isiterable(MAPPABLE)
    assert isiterable(SET)
    assert isiterable(STRING)
    assert isiterable(B_STRING)
    assert isiterable(U_STRING)
    assert isiterable(TUPLE)


def test_isiterable_not():
    assert not isiterable(False)
    assert not isiterable(FLOAT)
    assert not isiterable(INT)
    assert not isiterable(None)
    assert not isiterable(OBJECT)


def test_islistlike():
    assert islistlike(DICT)
    assert islistlike(IsListLike())
    assert islistlike(LIST)
    assert islistlike(MAPPABLE)


def test_islistlike_not():
    assert not islistlike(False)
    assert not islistlike(FLOAT)
    assert not islistlike(INT)
    assert not islistlike(None)
    assert not islistlike(OBJECT)
    assert not islistlike(SET)
    assert not islistlike(STRING)
    assert not islistlike(B_STRING)
    assert not islistlike(U_STRING)
    assert not islistlike(TUPLE)


def test_isnumber():
    assert isnumber(DECIMAL)
    assert isnumber(INT)
    assert isnumber(FLOAT)


def test_isnumber_not():
    assert not isnumber(DICT)
    assert not isnumber(False)
    assert not isnumber(None)
    assert not isnumber(LIST)
    assert not isnumber(OBJECT)
    assert not isnumber(SET)
    assert not isnumber(STRING)
    assert not isnumber(B_STRING)
    assert not isnumber(U_STRING)
    assert not isnumber(TUPLE)


def test_ispair():
    assert ispair(IsPair())
    assert ispair([1, 2])
    assert ispair({1, 2})
    assert ispair((1, 2))
    assert ispair("12")


def test_ispair_not():
    assert not ispair(DICT)
    assert not ispair(False)
    assert not ispair(IsSequence())
    assert not ispair(LIST)
    assert not ispair(MAPPABLE)
    assert not ispair(None)
    assert not ispair(OBJECT)
    assert not ispair(SET)
    assert not ispair(STRING)
    assert not ispair(B_STRING)
    assert not ispair(U_STRING)
    assert not ispair(TUPLE)


def test_ismappable():
    assert ismappable(DICT)
    assert ismappable(IsMappable())
    assert ismappable(MAPPABLE)


def test_ismappable_not():
    assert not ismappable(False)
    assert not ismappable(LIST)
    assert not ismappable(None)
    assert not ismappable(NotMappable())
    assert not ismappable(OBJECT)
    assert not ismappable(SET)
    assert not ismappable(STRING)
    assert not ismappable(B_STRING)
    assert not ismappable(U_STRING)
    assert not ismappable(TUPLE)


def test_ispathlike():
    assert ispathlike(STRING)
    assert ispathlike(B_STRING)
    assert ispathlike(U_STRING)
    assert ispathlike(LazyPath())


def test_ispathlike_not():
    assert not ispathlike(DICT)
    assert not ispathlike(False)
    assert not ispathlike(LIST)
    assert not ispathlike(None)
    assert not ispathlike(MAPPABLE)
    assert not ispathlike(OBJECT)
    assert not ispathlike(SET)
    assert not ispathlike(TUPLE)


def test_issequence():
    assert issequence(DICT)
    assert issequence(LIST)
    assert issequence(IsSequence())
    assert issequence(IsPair())
    assert issequence(MAPPABLE)
    assert issequence(SET)
    assert issequence(STRING)
    assert issequence(B_STRING)
    assert issequence(U_STRING)
    assert issequence(TUPLE)


def test_issequence_not():
    assert not issequence(False)
    assert not issequence(FLOAT)
    assert not issequence(INT)
    assert not issequence(None)
    assert not issequence(OBJECT)


def test_istuplike():
    assert istuplike(DICT)
    assert istuplike(IsTupLike())
    assert istuplike(IsListLike())
    assert istuplike(LIST)
    assert istuplike(MAPPABLE)
    assert istuplike(STRING)
    assert istuplike(B_STRING)
    assert istuplike(U_STRING)
    assert istuplike(TUPLE)


def test_istuplike_not():
    assert not istuplike(False)
    assert not istuplike(FLOAT)
    assert not istuplike(INT)
    assert not istuplike(None)
    assert not istuplike(OBJECT)


def test_iterable():
    assert DICT is iterable(DICT)
    assert LIST is iterable(LIST)
    assert MAPPABLE is iterable(MAPPABLE)
    assert SET is iterable(SET)
    assert STRING is iterable(STRING)
    assert TUPLE is iterable(TUPLE)

    assert [False] == iterable(False)
    assert [FLOAT] == iterable(FLOAT)
    assert [INT] == iterable(INT)
    assert [None] == iterable(None)
