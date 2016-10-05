﻿#!/usr/bin/env python
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

whitelist = []
gene = []
langkeywords = []


def parse_command_line():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=u'%(prog)s version 0.1'
    )
    parser.add_argument(
        '-g',
        '--gene',
        action='append',
        help='exlude word'
    )
    parser.add_argument(
        '-w',
        '--whitelist',
        help='whitelist file'
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


def is_whitelist(word):
    if word in whitelist:
        return True
    if word in langkeywords:
        return True
    # 辞書にあったら除外
    if word in gene:
        return True
    return False


def is_suspicion(word):
    length = len(word)
    # 1文字だけは除外
    if length <= 1:
        return False
    if not isalpha(word):
        return False
    if is_whitelist(word):
        return False
    # 過去形
    if length > 2 and word.endswith('ed'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
    # 進行形
    if length > 3 and word.endswith('ing'):
        if is_whitelist(word[:-3]):
            return False
        if is_whitelist(word[:-3] + 'e'):
            return False
    # 複数形
    if word.endswith('s'):
        if is_whitelist(word[:-1]):
            return False
    if length > 3 and word.endswith('ies'):
        if is_whitelist(word[:-3] + 'y'):
            return False
    return True


r_sign = re.compile('[!-/:-@[-`{-~]')
def text_transform(text):
    text = re.sub("([a-z0-9])([A-Z])(?=[a-z])", lambda x: x.group(1) + "_" + x.group(2), text)
    return re.sub(r_sign, ' ', text)


def checktagger(text, line, words):
    tags_plain = tagger.TagText(text)
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.word.lower()
        if is_suspicion(word):
            if words.has_key(word):
                words[word].append(line)
            else:
                words[word] = [line]


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    line_count = 1
    block_comment = False
    words = {}
    for line in f:
        text = line.strip()
        text, block_comment = checkcomment(text, block_comment)
        if not block_comment:
            if len(text) > 0:
                checktagger(text_transform(text), line_count, words)
        line_count += 1
    return words


def printresult(filepath, d):
    for k,v in sorted(d.items(), key=lambda x: len(x[1])):
        for line in v:
            print("{0}({1}): warning: \"{2}\": abbreviation ??".format(filepath, line, k))


def checkfile(f):
    global langkeywords
    langkeywords = keywords.getkeywords(f)
    words = check(f)
    printresult(f, words)


def checkdir(dir):
    for d in os.listdir(dir):
        d = os.path.join(dir, d)
        if os.path.isdir(d):
            checkdir(d)
        else:
            checkfile(d)


r_geneword = re.compile(r'^[a-zA-Z][a-z]+$')
def isgeneword(s):
    return r_geneword.match(s) is not None


def make_gene(file):
    f = open(file, 'r')
    for line in f:
        word = line.strip()
        if isgeneword(word):
            gene.append(word.lower())


def setup(options):
    global gene
    global whitelist
    if options.gene:
        for g in options.gene:
            gene.extend(make_gene(g))
    if options.whitelist:
        for word in options.whitelist:
            if isalpha(word):
                whitelist.append(word.lower())

def main():
    options, parser = parse_command_line()
    setup(options)
    for f in options.file:
        if os.path.isdir(f):
            checkdir(f)
        else:
            checkfile(f)


if __name__ == '__main__':
    main()
