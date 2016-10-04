#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import treetaggerwrapper
import keywords

from argparse import ArgumentParser

tagdir = os.getenv('TREETAGGER_ROOT')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=tagdir)
options = None

exclude = []
exclude_keywords = []


def parse_command_line():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=u'%(prog)s version 0.1'
    )
    parser.add_argument(
        '--html',
        action='store_true',
        help='output html'
    )
    parser.add_argument(
        '--exclude_keywords',
        action='store_true',
        help='exclude language keywords'
    )
    parser.add_argument(
        '--exclude',
        action='append',
        help='exlude word'
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


r_alpha = re.compile(r'^[a-zA-Z]+$')
def isalpha(s):
    return r_alpha.match(s) is not None


r_sign = re.compile('[!-/:-@[-`{-~]')
def text_transform(text):
    return re.sub(r_sign, ' ', text)


def checkword(word):
    if len(word) <= 1:
        return False
    if not isalpha(word):
        return False
    if word in exclude:
        return False
    if word in exclude_keywords:
        return False
    return True


def checktagger(text, line, words):
    # HogeFuga -> Hoge_Fuga
    text = re.sub("([a-z0-9])([A-Z])(?=[a-z])", lambda x: x.group(1) + "_" + x.group(2), text)
    tags_plain = tagger.TagText(text)
#    tags_plain = tagger.TagText(text, notagdns=True)
#    for tag in tags_plain:
#        print tag
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.word.lower()
        if checkword(word):
            if words.has_key(word):
                words[word].append(line)
            else:
                words[word] = [ line ]


def printwords(words):
    for k,v in sorted(words.items(), key=lambda x: len(x[1])):
        print("{0}: {1}".format(k, len(v)))


def printhtml(words):
    maxnum = len(max(words.values(), key=lambda x: len(x)))
    minnum = len(min(words.values(), key=lambda x: len(x)))
    diff = maxnum - minnum
    maxfontsize = 72
    minfontsize = 12
    difffontsize = maxfontsize - minfontsize
    def calcfontsize(num):
        return (num - minnum) * difffontsize / diff + minfontsize
    print('<html><body>')
    for k,v in sorted(words.items(), key=lambda x: x[0]):
        print('<span style="font-size: {0}px">{1}</span>'.format(calcfontsize(len(v)), k))
    print('</body></html>')


r_block_comment_begin = re.compile('(.*)/\*.*')
r_block_comment_end = re.compile('.*\*/(.*)')
line_comment = '//'


def checkcomment(text, block_comment):
    if block_comment:
        m = r_block_comment_end.match(text)
        if m:
            block_comment = False
            text = m.group(1)
    if not block_comment:
        m = r_block_comment_begin.match(text)
        if m:
            block_comment = True
            text = m.group(1)
        line_comment_start = text.find(line_comment)
        if line_comment_start != -1:
            text = text[:line_comment_start]
    return text, block_comment


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    line_count = 1
    block_comment = False
    words = {}
    for line in f:
        #print(str(count) + ':' + line)
        text = line.strip()
        text, block_comment = checkcomment(text, block_comment)
        if not block_comment:
            if len(text) > 0:
                checktagger(text_transform(text), line_count, words)
        line_count += 1
    if options.html:
        printhtml(words)
    else:
        printwords(words)


def checkfile(f):
    global exclude_keywords
    if options.exclude_keywords:
        exclude_keywords = keywords.getkeywords(f)
    check(f)


def checkdir(dir):
    for d in os.listdir(dir):
        d = os.path.join(dir, d)
        if os.path.isdir(d):
            checkdir(d)
        else:
            checkfile(d)


def main():
    global options
    global exclude
    options, parser = parse_command_line()
    if options.exclude:
        for e in options.exclude:
            exclude.extend(e.split(','))
    for f in options.file:
        if os.path.isdir(f):
            checkdir(f)
        else:
            checkfile(f)


if __name__ == '__main__':
    main()
