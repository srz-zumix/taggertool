#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import treetaggerwrapper
import requests
import unicodedata

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

class Location:
    def __init__(self, file, line):
        self.file = file
        self.line = line


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
        metavar='FILE',
        help='exlude word'
    )
    parser.add_argument(
        '-w',
        '--whitelist',
        action='append',
        metavar='FILE',
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
        metavar='NAME',
        help='load translation cache'
    )
    parser.add_argument(
        '--cache-dir',
        default=None,
        metavar='DIR',
        help='translation cache directory'
    )
    parser.add_argument(
        '--list-all',
        action='store_true',
        help='list up all location'
    )
    parser.add_argument(
        '--ignore-noexists',
        action='store_true',
        help='ignore option file not exists'
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


r_alphasign = re.compile(r'^[!-~]+$')
def isalphasign(s):
    return r_alphasign.match(s) is not None


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
        print("Http error:", e.message)
        if e.response.status_code == 429:
            print("request count: ", Glosbe.count)
            options.glosbe = False
        else:
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


def is_abbreviation_dejizo_word_impl(body):
    #if u'化学記号' in body:
    #    return True
    #if u'（…）' in body:
    #    return True
    # 英数と特定の記号のみなら略語とする
    # e.g. =refarence
    nbody = unicodedata.normalize('NFKC', body)
    if isalphasign(nbody):
        return True
    return False


def is_abbreviation_dejizo_impl(search_result, dict):
    ids = Dejizo.result_to_ids(search_result)
    if len(ids) == 0:
        return False
    for id in ids:
        r = Dejizo.get(id, dict)
        body = Dejizo.get_body(r).strip()
        if not is_abbreviation_dejizo_word_impl(body):
            return False
    return True


# retval  0 = ヒット
# retval  1 = ノーヒット
# retval -1 = 略語
def is_suspicion_dejizo_impl(word, dict):
    try:
        r = Dejizo.search(word, dict)
        d = Dejizo.response_to_result(r)
        if d['ok'] and 'SearchDicItemResult' in d:
            result = d['SearchDicItemResult']
            count = int(result['ItemCount'])
            if count > 0:
                if len(word) > 4:
                    return 0
                # 短い単語は詳細を get して調べる
                if Dejizo.is_getable(word, dict):
                    try:
                        if is_abbreviation_dejizo_impl(d, dict):
                            service_cache['dejizo'].add_abbreviation(word)
                            return -1
                        else:
                            return 0
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        pass
    except:
        pass
    return 1


def is_suspicion_dejizo(word):
    # 2文字以下は略語かどうかの判別がつけにくいため除外
    if len(word) <= 2:
        return False
    # どちらかの辞書に略語としてあったら即時 True
    ret = is_suspicion_dejizo_impl(word, Dejizo.DailyEJL)
    if ret < 0:
        return True
    ret2 = is_suspicion_dejizo_impl(word, Dejizo.EJdict)
    if ret2 < 0:
        return True
    # どちらの辞書にもなかったら True
    if ret > 0 and ret2 > 0:
        return True
    # どちらかの辞書にあったらキャッシュに登録
    service_cache['dejizo'].add(word)
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
r_transform = re.compile('([a-z0-9])([A-Z])(?=[A-Z]*[a-z\s]|$)')
def text_transform(text):
    text = re.sub(r_sign, ' ', text)
    text = re.sub(r_transform, lambda x: x.group(1) + " " + x.group(2), text)
    return text


def checktagger(filepath, text, line):
    global words
    global checked_words
    tags_plain = tagger.TagText(text)
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.word.lower()
        if not word in checked_words:
            location = Location(filepath, line)
            if words.has_key(word):
                words[word].append(location)
            elif is_suspicion(word):
                words[word] = [location]
            else:
                checked_words.append(word)


def readline(f):
    try:
        return f.readline()
    except:
        return ""


def check(filepath):
    filename = os.path.basename(filepath)
    f = codecs.open(filepath, 'r', encoding='utf-8-sig')
    print('check: {0}'.format(filename))
    line_count = 1
    block_comment = False
    line = readline(f)
    while line:
        text = line.strip()
        text, block_comment = checkcomment(text, block_comment)
        if not block_comment:
            if len(text) > 0:
                checktagger(filepath, text_transform(text), line_count)
        line_count += 1
        line = readline(f)
    f.close()


def printresult():
    if options.list_all:
        for k,v in sorted(words.items(), key=lambda x: len(x[1])):
            for location in v:
                print("{0}({1}): warning: \"{2}\": is ok ??".format(location.file, location.line, k))
    else:
        for k,v in sorted(words.items(), key=lambda x: x[0]):
            location = v[0]
            if len(v) > 1:
                print("{0}({1}): warning: \"{2}\": is ok ?? ({3})".format(location.file, location.line, k, len(v)))
            else:
                print("{0}({1}): warning: \"{2}\": is ok ??".format(location.file, location.line, k))
        print("Total number detected: {0}".format(len(words)))


def checkfile(f):
    global langkeywords
    langkeywords = keywords.getkeywords(f)
    check(f)


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
    if not options.ignore_noexists or os.path.exists(file):
        f = open(file, 'r')
        for line in f:
            word = line.strip()
            if isgeneword(word):
                gene.append(word.lower())
    return gene


def make_wordlist(file):
    wordlist = []
    if not options.ignore_noexists or os.path.exists(file):
        f = open(file, 'r')
        for line in f:
            word = line.strip()
            if isalpha(word):
                wordlist.append(word.lower())
    else:
        print(file + ': ignore')
    return wordlist


def setup_cache(name):
    cache = Cache(name)
    cache.setup(options.cache_dir)
    service_cache[name] = cache


def setup():
    global gene
    global whitelist
    global abbreviations
    if options.cache_dir is None:
        options.cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
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
            setup_cache('glosbe')
        if options.dejizo:
            setup_cache('dejizo')
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
    printresult()
    print('==== end ====')

if __name__ == '__main__':
    main()
