#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import treetaggerwrapper
import requests

import keywords

from dejizo import Dejizo
from glosbe import Glosbe
from argparse import ArgumentParser
    
tagdir = os.getenv('TREETAGGER_ROOT')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=tagdir)
options = None

whitelist = []
gene = []
abbreviations = []
langkeywords = []

class Cache:
    gene = []
    abbreviations = []
    gene_file = None
    abbreviations_file = None

    def __init__(self, name):
        self.name = name

    def setup(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        self._load(dir, 'a+')

    def load(self, dir):
        self._load(dir)

    def _load(self, dir, mode):
        self._open(dir, mode)
        for w in self.gene_file:
            self.gene.append(w.rstrip())
        for w in self.abbreviations_file:
            self.abbreviations.append(w.rstrip())

    def _open(self, dir, mode):
        self.gene_file = open(Cache.get_gene_filename(dir, self.name), mode)
        self.abbreviations_file = open(Cache.get_abbreviation_filename(dir, self.name), mode)

    @staticmethod
    def get_gene_filename(dir, name):
        return dir + '/' + name + '.txt'

    @staticmethod
    def get_abbreviation_filename(dir, name):
        return dir + '/' + name + '_abbreviations.txt'

    def add(self, word):
        if self.gene_file:
            self.gene_file.write(word + '\n')
            self.gene_file.flush()

    def add_abbreviation(self, word):
        if self.abbreviations_file:
            self.abbreviations_file.write(word + '\n')
            self.abbreviations_file.flush()


service_cache = {}
words = {}
checked_words = []


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
        action='append',
        help='whitelist file'
    )
    parser.add_argument(
        '-e',
        '--exclude',
        action='append',
        help='exlude word'
    )
    parser.add_argument(
        '-a',
        '--abbreviation',
        action='append',
        help='abbreviation word'
    )
    parser.add_argument(
        '--glosbe',
        action='store_true',
        help='use online translation service (glosbe)'
    )
    parser.add_argument(
        '--dejizo',
        action='store_true',
        help='use online service (dejizo)'
    )
    parser.add_argument(
        '--cache',
        action='store_true',
        help='online translation cache enable'
    )
    parser.add_argument(
        '--load-cache',
        action='append',
        help='load translation cache'
    )
    parser.add_argument(
        '--cache-dir',
        default='cache',
        help='translation cache directory'
    )
    parser.add_argument(
        '--list-words',
        action='store_true',
        help='list up words only'
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


def is_suspicion_glosbe_impl(word):
    try:
        r = Glosbe.Translate(word, Glosbe.EN, Glosbe.JA)
        if r['result'] == 'ok':
            tuc = r['tuc']
            if len(tuc) == 0:
                return True
            for t in tuc:
                # 1 の辞書だけ使う
                if 1 in t['authors']:
                    for meaning in t['meanings']:
                        if meaning['language'] == Glosbe.EN:
                            # XXX の略語って意味はダメ
                            if 'abbreviation' in meaning['text']:
                                service_cache['glosbe'].add_abbreviation(word)
                                return True
                    service_cache['glosbe'].add(word)
                    return False
    except requests.HTTPError as e:
        if e.response.status_code == 429:
            print("request count: ", Glosbe.count)
        print("Http error:", e.message)
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return True


def is_suspicion_glosbe(word):
    if is_suspicion_glosbe_impl(word):
        return True
    else:
        return False


def is_suspicion_dejizo_impl(word):
    try:
        r = Dejizo.search(word)
        print Dejizo.response_to_result(r)
    except:
        pass
    return False


def is_suspicion_dejizo(word):
    if is_suspicion_dejizo_impl(word):
        return True
    else:
        return False


def is_whitelist(word):
    if word in whitelist:
        return True
    if word in langkeywords:
        return True
    # 辞書にあったら除外
    if word in gene:
        return True
    for cache in service_cache.values():
        if word in cache.gene:
            return True
    return False


def is_suspicion_past(word, length):
    if length > 2 and word.endswith('ed'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if length > 3 and word.endswith('ied'):
            if is_whitelist(word[:-3] + 'y'):
                return False
        if re.match('.*[a-z]{2,2}ed$', word):
            if is_whitelist(word[:-3]):
                return False
        if length > 4 and word.endswith('cked'):
            if is_whitelist(word[:-3]):
                return False
    return True


def is_suspicion_past_participle(word, length):
    if length > 2 and word.endswith('en'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if re.match('.*[a-z]{2,2}en$', word):
            if is_whitelist(word[:-3]):
                return False
            if is_whitelist(word[:-3] + 'e'):
                return False
    return True


def is_suspicion_post_suffix(word, length):
    # er
    if length > 2 and word.endswith('er'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if length > 3 and word.endswith('ier'):
            if is_whitelist(word[:-3] + 'y'):
                return False
        if re.match('.*[a-z]{2,2}er$', word):
            if is_whitelist(word[:-3]):
                return False
            if is_whitelist(word[:-3] + 'e'):
                return False
    # or
    if length > 2 and word.endswith('or'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-2] + 'e'):
            return False
    # ist
    if length > 3 and word.endswith('ist'):
        if is_whitelist(word[:-3]):
            return False
    # ant
    if length > 3 and word.endswith('ant'):
        if is_whitelist(word[:-3]):
            return False
        if is_whitelist(word[:-3] + 'y'):
            return False
    return True


def is_suspicion_pre_suffix(word, length):
    # un
    if length > 2 and word.startswith('un'):
        if is_whitelist(word[2:]):
            return False
    # re
    if length > 2 and word.startswith('re'):
        if is_whitelist(word[2:]):
            return False
    return True


def is_suspicion_progressive(word, length):
    if length > 3 and word.endswith('ing'):
        if is_whitelist(word[:-3]):
            return False
        if is_whitelist(word[:-3] + 'e'):
            return False
        if re.match('.*[a-z]{2,2}ing$', word):
            if is_whitelist(word[:-4]):
                return False
    return True


def is_suspicion_plural(word, length):
    if word.endswith('s'):
        if is_whitelist(word[:-1]):
            return False
        if length > 2 and word.endswith('es'):
            if is_whitelist(word[:-2]):
                return False
        if length > 3 and word.endswith('ies'):
            if is_whitelist(word[:-3] + 'y'):
                return False
    return True


def is_suspicion(word):
    length = len(word)
    # 1文字だけは除外
    if length <= 1:
        return False
    if not isalpha(word):
        return False
    if is_whitelist(word):
        return False
    # 略語リストにあったら即アウト
    for cache in service_cache.values():
        if word in cache.abbreviations:
            return True
    # 過去形
    if not is_suspicion_past(word, length):
        return False
    # 過去分詞
    if not is_suspicion_past_participle(word, length):
        return False
    # 進行形
    if not is_suspicion_progressive(word, length):
        return False
    # 複数形
    if not is_suspicion_plural(word, length):
        return False
    # 接頭辞
    if not is_suspicion_pre_suffix(word, length):
        return False
    # 接尾辞
    if not is_suspicion_post_suffix(word, length):
        return False
    # Web API
    if options.glosbe:
        if not is_suspicion_glosbe(word):
            return False
    if options.dejizo:
        if not is_suspicion_dejizo(word):
            return False
    return True


r_sign = re.compile('[!-/:-@[-`{-~]')
def text_transform(text):
    text = re.sub("([a-z0-9])([A-Z])(?=[a-z])", lambda x: x.group(1) + "_" + x.group(2), text)
    return re.sub(r_sign, ' ', text)


def checktagger(text, line):
    global words
    global checked_words
    tags_plain = tagger.TagText(text)
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.word.lower()
        if not word in checked_words:
            if words.has_key(word):
                words[word].append(line)
            elif is_suspicion(word):
                words[word] = [line]
            else:
                checked_words.append(word)


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    line_count = 1
    block_comment = False
    for line in f:
        text = line.strip()
        text, block_comment = checkcomment(text, block_comment)
        if not block_comment:
            if len(text) > 0:
                checktagger(text_transform(text), line_count)
        line_count += 1


def printresult(filepath):
    if options.list_words:
        for k,v in sorted(words.items(), key=lambda x: len(x[1])):
            print("{0}(N): warning: \"{1}\": is ok ??".format(filepath, k))
    else:
        for k,v in sorted(words.items(), key=lambda x: len(x[1])):
            for line in v:
                print("{0}({1}): warning: \"{2}\": is ok ??".format(filepath, line, k))


def checkfile(f):
    global langkeywords
    langkeywords = keywords.getkeywords(f)
    check(f)
    printresult(f)


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
    gene = []
    f = open(file, 'r')
    for line in f:
        word = line.strip()
        if isgeneword(word):
            gene.append(word.lower())
    return gene


def make_wordlist(file):
    wordlist = []
    f = open(file, 'r')
    for line in f:
        word = line.strip()
        if isalpha(word):
            wordlist.append(word.lower())
    return wordlist


def setup():
    global gene
    global whitelist
    global abbreviations
    if options.gene:
        for g in options.gene:
            gene.extend(make_gene(g))
    if options.whitelist:
        for w in options.whitelist:
            whitelist.extend(make_wordlist(w))
    if options.abbreviation:
        for f in options.abbreviation:
            abbreviations.extend(make_wordlist(f))
    if options.cache:
        if options.glosbe:
            cache = Cache('glosbe')
            cache.setup(options.cache_dir)
            service_cache['glosbe'] = cache
        if options.dejizo:
            cache = Cache('dejizo')
            cache.setup(options.cache_dir)
            service_cache['dejizo'] = cache
    if options.exclude:
        for e in options.exclude:
            whitelist.extend(e.split(','))
    if options.load_cache:
        for f in options.load_cache:
            whitelist.extend(make_wordlist(Cache.get_gene_filename(options.cache_dir, f)))
            abbreviations.extend(make_wordlist(Cache.get_abbreviation_filename(options.cache_dir, f)))


def main():
    global options
    options, parser = parse_command_line()
    setup()
    for f in options.file:
        if os.path.isdir(f):
            checkdir(f)
        else:
            checkfile(f)


if __name__ == '__main__':
    main()
