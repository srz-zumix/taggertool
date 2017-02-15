#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import unicodedata

import keywords

class FileReader(object):
    Keywords = []

    def __init__(self):
        self.file = None
        self.keywords = []
        self.pglang = None

    def open(self, filepath, encoding=None):
        if self.is_open():
            self.close()
        if encoding:
            self.file = codecs.open(filepath, 'r', encoding=encoding)
        else:
            self.file = codecs.open(filepath, 'r')
        self.keywords = keywords.getkeywords(filepath)
        self.pglang = keywords.getlanguage(filepath)

    def close(self):
        if self.file:
            self.file.close()

    def is_open(self):
        return self.file != None

    def __readline(self):
        try:
            return self.file.readline()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return None

    def readline(self):
        return self.__readline()

    def getsize(self):
        return os.path.getsize(self.file.name)

    def getlanguage(self):
        return self.pglang

    def getkeywords(self):
        return self.keywords

    def tell(self):
        return self.file.tell()


class SourceCodeReader(FileReader):
    block_comment = False

    def __init__(self, r_block_comment_begin, r_block_comment_end, line_comment):
        self.r_block_comment_begin = r_block_comment_begin
        self.r_block_comment_end = r_block_comment_end
        self.line_comment = line_comment
        super(SourceCodeReader, self).__init__()

    def readline(self):
        text = super(SourceCodeReader, self).readline()
        if not text:
            return text
        if self.block_comment:
            m = self.r_block_comment_end.match(text)
            if m:
                self.block_comment = False
                text = m.group(1)
            else:
                text = ' '
        if not self.block_comment:
            m = self.r_block_comment_begin.match(text)
            if m:
                self.block_comment = True
                text = m.group(1)
            line_comment_start = text.find(self.line_comment)
            if line_comment_start != -1:
                text = text[:line_comment_start]
        if not text:
            # not EOF
            return ' '
        return text


class CppFileReader(SourceCodeReader):
    def __init__(self):
        r_block_comment_begin = re.compile('(.*)/\*.*')
        r_block_comment_end = re.compile('.*\*/(.*)')
        line_comment = '//'
        super(CppFileReader, self).__init__(r_block_comment_begin, r_block_comment_end, line_comment)


def CreateFileReader(filepath):
    pglang = keywords.getlanguage(filepath)
    if pglang == 'c++':
        return CppFileReader()
    return FileReader()


def OpenFile(filepath, encoding=None):
    f = CreateFileReader(filepath)
    if f:
        f.open(filepath, encoding)
    return f

