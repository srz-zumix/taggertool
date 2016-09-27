#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs

from argparse import ArgumentParser

has_error = False

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


def checktagger(text):


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    count = 0
    for line in f:
        print(str(count) + ':' + line)
        text = line.strip()
        if len(text) > 0 and not text.startswith('//'):
            checktagger(text)
        count += 1


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
    if has_error:
        sys.exit(1)
