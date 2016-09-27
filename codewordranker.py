#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import treetaggerwrapper

from argparse import ArgumentParser

tagdir = os.getenv('TREETAGGER_ROOT')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=tagdir)

def parse_command_line():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=u'%(prog)s version 0.1'
    )
    parser.add_argument(
        'file',
        metavar='FILE/DIR',
        nargs='+',
        help='source code file/dir'
    )
    options = parser.parse_args()
    return options, parser

r_alnum = re.compile(r'^[a-zA-Z0-9]+$')
def isalnum(s):
    return r_alnum.match(s) is not None

def checkword(word):
    if not isalnum(word):
        return False
    return True

def checktagger(text, line, words):
    tags_plain = tagger.TagText(text)
#    tags_plain = tagger.TagText(text, notagdns=True)
#    for tag in tags_plain:
#        print tag
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.lemma
        if checkword(word):
            if words.has_key(word):
                words[word].append(line)
            else:
                words[word] = [ line ]


def printwords(words):
    for k,v in sorted(words.items(), key=lambda x: len(x[1])):
        print("{0}: {1}".format(k, len(v)))


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    line_count = 0
    words = {}
    for line in f:
        #print(str(count) + ':' + line)
        text = line.strip()
        if len(text) > 0 and not text.startswith('//'):
            checktagger(text, line_count, words)
        line_count += 1
    printwords(words)


def checkfile(f):
    check(f)


def checkdir(dir):
    for d in os.listdir(dir):
        d = os.path.join(dir, d)
        if os.path.isdir(d):
            checkdir(d)
        else:
            checkfile(d)

def main():
    options, parser = parse_command_line()
    for f in options.file:
        if os.path.isdir(f):
            checkdir(f)
        else:
            checkfile(f)


if __name__ == '__main__':
    main()
