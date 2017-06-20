#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

commonwords =  [ 'alpha'
                , 'ascii'
                , 'beta'
                , 'cygwin'
                , 'copyright'
                , 'cpplint'
                , 'cuda'
                , 'csv'
                , 'cpu'
                , 'crypto'
                , 'dot'
                , 'doxygen'
                , 'endian'
                , 'euc'
                , 'fpu'
                , 'freebsd'
                , 'giga'
                , 'git'
                , 'google'
                , 'http'
                , 'https'
                , 'iphone'
                , 'jis'
                , 'jpeg'
                , 'jpg'
                , 'junit'
                , 'kilo'
                , 'linux'
                , 'macro'
                , 'mega'
                , 'microsoft'
                , 'mingw'
                , 'mono'
                , 'mwerks'
                , 'nacl'
                , 'peta'
                , 'pico'
                , 'png'
                , 'posix'
                , 'ppapi'
                , 'regex'
                , 'shiftjis'
                , 'solaris'
                , 'sunos'
                , 'svn'
                , 'tera'
                , 'todo'
                , 'unicode'
                , 'url'
                , 'utf'
                , 'unix'
                , 'wandbox'
                , 'xterm'
                ]

xmlwords = [  'xml'
            , 'xmlattribute'
            , 'xmldata'
            , 'xmldocument'
            , 'xmlelement'
            , 'xmlerror'
            , 'xmlfooter'
            , 'xmlheader'
            , 'xmlprinter'
           ]

doxygenwords = [ 'retval'
            ]

cppext = [ '.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx', '.ipp' ]
csext = [ '.cs' ]
objcext = [ '.mm', '.m' ]
diffext = [ '.diff', '.patch' ]
loaded = []

def _load_dir(dir):
    if dir in loaded:
        return
    root = os.path.join(os.path.join(os.path.dirname(__file__), 'keywords'), dir)
    if not os.path.exists(root):
        return
    for filename in os.listdir(root):
        path = os.path.join(root, filename)
        if os.path.isfile(path):
            basename = os.path.basename(path)
            name, ext = os.path.splitext(basename)
            var_name = dir + '_' + name
            f = open(path, 'r')
            words = []
            for w in f:
                words.append(w.rstrip())
            globals()[var_name] = words
    loaded.append(dir)


def appendix(d):
    for word in d:
        if '_' in str(word):
            #d.append(word.replace('_', ''))
            for s in word.split('_'):
                if len(s) > 2 and s not in d:
                    d.append(s)


def extend_keywords(keywords, add):
    keywords.extend([ str(s).lower() for s in add if not s.startswith('#') ])


def make_cppkeywords():
    _load_dir('cpp')
    langkeywords = commonwords
    for name, v in globals().items():
        if name.startswith('cpp_') and isinstance(v, list): 
            extend_keywords(langkeywords, v)
    extend_keywords(langkeywords, xmlwords)
    extend_keywords(langkeywords, doxygenwords)
    appendix(langkeywords)
    langkeywords.sort()
    return langkeywords


def make_csharpkeywords():
    _load_dir('cs')
    langkeywords = commonwords
    for name, v in globals().items():
        if name.startswith('cs_') and isinstance(v, list): 
            extend_keywords(langkeywords, v)
    appendix(langkeywords)
    langkeywords.sort()
    return langkeywords


def make_objckeywords():
    _load_dir('cpp')
    langkeywords = commonwords
    for name, v in globals().items():
        if name.startswith('cpp_') and not 'win' in name and isinstance(v, list): 
            extend_keywords(langkeywords, v)
    appendix(langkeywords)
    langkeywords.sort()
    return langkeywords


def make_defaultkeywords():
    langkeywords = commonwords
    appendix(langkeywords)
    return langkeywords


cppkeywords_all = None
csharpkeywords_all = None
objckeywords_all = None
defaultkeywords_all = None

supported_languages = [ 'c++', 'c#', 'objc', 'diff' ]

def getlanguage_from_ext(ext):
    if ext in cppext:
        return 'c++'
    elif ext in csext:
        return 'c#'
    elif ext in objcext:
        return 'objc'
    elif ext in diffext:
        return 'diff'
    return None


def getlanguage(file):
    if file is None:
        return None
    root, ext = os.path.splitext(file)
    return getlanguage_from_ext(ext)


def getkeywords_from_language(lang):
    global cppkeywords_all
    global csharpkeywords_all
    global objckeywords_all
    global defaultkeywords_all
    if lang == 'c++':
        if cppkeywords_all is None:
            cppkeywords_all = make_cppkeywords()
        return cppkeywords_all
    elif lang == 'c#':
        if csharpkeywords_all is None:
            csharpkeywords_all = make_csharpkeywords()
        return csharpkeywords_all
    elif lang == 'obj-c':
        if objckeywords_all is None:
            objckeywords_all = make_objckeywords()
        return objckeywords_all

    if defaultkeywords_all is None:
        defaultkeywords_all = make_defaultkeywords()
    return defaultkeywords_all


def getkeywords_from_ext(ext):
    return getkeywords_from_language(getlanguage_from_ext(ext))


def getkeywords(file):
    return getkeywords_from_language(getlanguage(file))



#
#
def export_list(list, filepath):
    f = open(filepath, 'w')
    for w in sorted(set(list)):
        f.write(str(w) + '\n')


def _export_dir(dir):
    root = os.path.join('keywords', dir)
    if not os.path.exists(root):
        os.makedirs(root)
    for name, v in globals().items():
        if name.startswith(dir + '_') and isinstance(v, list):
            filename = '{1}.txt'.format(dir, name[len(dir)+1:])
            export_list(v, os.path.join(root, filename))


def _load():
    _load_dir('cs')
    _load_dir('cpp')


def _export():
    _load()
    _export_dir('cpp')
    _export_dir('cs')


if __name__ == '__main__':
    argv = sys.argv[1:]
    if 'sort' in argv:
        _export()
    if 'print' in argv:
        print(make_cppkeywords())
        print(make_csharpkeywords())
        print(make_objckeywords())
    if 'cpp' in argv:
        print(make_cppkeywords())
    if 'objc' in argv:
        print(make_objckeywords())
    if 'cs' in argv:
        print(make_csharpkeywords())

