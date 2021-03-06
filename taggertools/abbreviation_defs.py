#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RequestLimitError(Exception):
    pass


class MisspellingError(Exception):
    pass


class IgnoreError(Exception):
    pass


class InflectedError(Exception):
    def __init__(self, word):
        self.message = word


class PluralError(InflectedError):
    def __init__(self, word):
        super(PluralError, self).__init__(word)


class PastError(InflectedError):
    def __init__(self, word):
        super(PastError, self).__init__(word)


class DictResult:
    Found = 0
    NoCheck = 1
    Abbreviation = -1
    NotFound = -2
    Misspelling = -3

    @staticmethod
    def is_suspicion(r):
        if r >= 0:
            return False
        return True


class WordResult:
    def __init__(self, r, location):
        self.result = r
        self.locations = [ location ]

    def add_location(self, location):
        self.locations.append(location)
