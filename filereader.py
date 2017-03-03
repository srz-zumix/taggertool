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
        self.keywords = None
        self.pglang = None
        self.rawline = None

    def open(self, filepath, encoding=None):
        if self.is_open():
            self.close()
        if encoding:
            self.file = codecs.open(filepath, 'r', encoding=encoding)
        else:
            self.file = codecs.open(filepath, 'r')
        if self.pglang is None:
            self.pglang = keywords.getlanguage(filepath)
        if self.keywords is None:
            self.keywords = keywords.getkeywords_from_language(self.pglang)

    def close(self):
        if self.file:
            self.file.close()

    def is_open(self):
        return self.file != None

    def __readline(self):
        try:
            self.rawline = self.file.readline()
            return self.rawline
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return None

    def readline(self):
        return self.__readline()

    def getrawline(self):
        return self.rawline

    def getsize(self):
        return os.path.getsize(self.file.name)

    def setlanguage(self, lang):
        self.pglang = lang

    def getlanguage(self):
        return self.pglang

    def getkeywords(self):
        return self.keywords

    def tell(self):
        return self.file.tell()


class SourceCodeReader(FileReader):
    block_comment = False

    def __init__(self, block_comment_begin, block_comment_end, line_comment):
        self.r_block_comment_begin = re.compile('(.*)' + block_comment_begin + '.*')
        self.r_block_comment_end = re.compile('.*' + block_comment_end + '(.*)')
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
        block_comment_begin = '/\*'
        block_comment_end = '\*/'
        line_comment = '//'
        super(CppFileReader, self).__init__(block_comment_begin, block_comment_end, line_comment)
        self.pglang = 'c++'


class ObjCFileReader(CppFileReader):
    def __init__(self):
        super(ObjCFileReader, self).__init__()
        self.pglang = 'objc'


class CSharpFileReader(SourceCodeReader):
    def __init__(self):
        block_comment_begin = '/\*'
        block_comment_end = '\*/'
        line_comment = '//'
        super(CSharpFileReader, self).__init__(block_comment_begin, block_comment_end, line_comment)
        self.pglang = 'c#'


class DiffFileReader(FileReader):
    def __init__(self):
        super(DiffFileReader, self).__init__()

    def open(self, filepath, encoding=None):
        if self.is_open():
            self.close()
        if encoding:
            self.file = codecs.open(filepath, 'r', encoding=encoding)
        else:
            self.file = codecs.open(filepath, 'r')

    def update_keywords(self, filename):
        self.keywords = keywords.getkeywords(filename)
        self.pglang = keywords.getlanguage(filename)

    def readline(self):
        text = super(DiffFileReader, self).readline()
        if not text:
            return text
        if text.startswith('+'):
            if not text.startswith('+++ '):
                return text[1:]
        if text.startswith('diff '):
            filename = text.split()[-1]
            self.update_keywords(filename)
        # not EOF
        return ' '


def CreateFileReader(filepath, language=None):
    if language is None:
        language = keywords.getlanguage(filepath)
    if language == 'c++':
        return CppFileReader()
    elif language == 'objc':
        return ObjCFileReader()
    elif language == 'c#':
        return CSharpFileReader()
    else:
        root, ext = os.path.splitext(filepath)
        if ext in ['.diff', '.patch']:
            return DiffFileReader()

    return FileReader()


def OpenFile(filepath, encoding=None, language=None):
    f = CreateFileReader(filepath, language)
    if f:
        f.open(filepath, encoding)
    return f

