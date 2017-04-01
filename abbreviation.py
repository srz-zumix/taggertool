#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import codecs
import requests
import unicodedata
import argparse
import shutil

import keywords
import filereader

from dejizo import Dejizo
from glosbe import Glosbe
from argparse import ArgumentParser
from difflib import SequenceMatcher

try:
    #import treetaggerwrapper
    #tagdir = os.getenv('TREETAGGER_ROOT')
    #tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=tagdir)
    tagger = None
except:
    tagger = None

options = None

whitelist = []
gene = []
abbreviations = []
langkeywords = []
default_encoding = 'utf-8-sig'
prev_detect_encoding = ''
default_encoding_change_count = 0

exclude_dir = [ '.git', '.svn', '.vs', 'temp', 'tmp' ]

class Location:
    current_path = None

    def __init__(self, file, line):
        self.file = file
        self.line = line
        if file:
            if Location.current_path:
                self.relpath = os.path.relpath(file, Location.current_path)
            else:
                self.relpath = os.path.basename(file)
        else:
            self.relpath = None


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
        self._load(dir)
        self._open(dir, 'a')

    def load(self, dir):
        self._load(dir)

    def _load(self, dir):
        path = Cache.get_gene_filename(dir, self.name)
        if os.path.exists(path):
            f = open(path, 'r')
            for w in f:
                self.gene.append(w.rstrip())
            f.close()
        path = Cache.get_abbreviation_filename(dir, self.name)
        if os.path.exists(path):
            f = open(path, 'r')
            for w in f:
                self.abbreviations.append(w.rstrip())
            f.close()

    def _open(self, dir, mode):
        self.gene_file = open(Cache.get_gene_filename(dir, self.name), mode)
        self.abbreviations_file = open(Cache.get_abbreviation_filename(dir, self.name), mode)

    def _close(self):
        if self.gene_file:
            self.gene_file.close()
        if self.abbreviations_file:
            self.abbreviations_file.close()

    @staticmethod
    def get_gene_filename(dir, name):
        return dir + '/' + name + '.txt'

    @staticmethod
    def get_abbreviation_filename(dir, name):
        return dir + '/' + name + '_abbreviations.txt'

    @staticmethod
    def islock(dir, name):
        for f in Cache.get_files(dir, name):
            if os.path.exists(f + '.lock'):
                return True
        return False

    @staticmethod
    def lock(dir, name):
        if not Cache.islock(dir, name):
            for f in Cache.get_files(dir, name):
                shutil.copy(f, f + '.lock')

    @staticmethod
    def unlock(dir, name):
        for f in Cache.get_files(dir, name):
            lockfile = f + '.lock'
            if os.path.exists(lockfile):
                os.remove(lockfile)

    @staticmethod
    def get_files(dir, name):
        return [ Cache.get_gene_filename(dir, name), Cache.get_abbreviation_filename(dir, name) ]

    def add(self, word):
        self.gene.append(word)
        if self.gene_file:
            self.gene_file.write(word + '\n')
            self.gene_file.flush()

    def add_abbreviation(self, word):
        self.abbreviations.append(word)
        if self.abbreviations_file:
            self.abbreviations_file.write(word + '\n')
            self.abbreviations_file.flush()


class DictResult:
    Found = 0
    NoCheck = 1
    Abbreviation = -1
    NotFound = -2

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


service_cache = {}
words = {}
checked_words = []
cache_choices = ['glosbe', 'dejizo']


def add_abbreviation(dict, word):
    if dict in service_cache:
        service_cache[dict].add_abbreviation(word)


def add_cache(dict, word):
    if dict in service_cache:
        service_cache[dict].add(word)


def parse_command_line():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=u'%(prog)s version 0.2'
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
        choices=cache_choices,
        help='load translation cache'
    )
    parser.add_argument(
        '--cache-dir',
        default=None,
        metavar='DIR',
        help='translation cache directory'
    )
    parser.add_argument(
        '--disable-keywords',
        action='store_true',
        help='disable general and language keywords'
    )
    parser.add_argument(
        '--cache-rebuild',
        choices=cache_choices,
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '-x',
        '--language',
        choices=keywords.supported_languages,
        help='select language'
    )
    parser.add_argument(
        '--list-all',
        action='store_true',
        help='list up all location'
    )
    parser.add_argument(
        '--progress',
        action='store_true',
        help='print percent progress'
    )
    parser.add_argument(
        '--safe-mode',
        action='store_true',
        help='api request limit safe mode(glosbe)'
    )
    parser.add_argument(
        '--no-request-limit',
        action='store_true',
        help=argparse.SUPPRESS
#        help='no api request limit'
    )
    parser.add_argument(
        '--encoding',
        default=None,
        help='set file encoding'
    )
    parser.add_argument(
        '--extension',
        default='(c|h|cpp|hpp|cxx|hxx|cc|hh|ipp|cu|m|mm|cs|diff|patch)$',
        help='file extension matcher'
    )
    parser.add_argument(
        '--ignore-noexists',
        action='store_true',
        help='ignore option file not exists'
    )
    parser.add_argument(
        '--relpath',
        action='store_true',
        help='print relative path'
    )
    parser.add_argument(
        'file',
        metavar='FILE/DIR',
        nargs='*',
        help='source code file/dir'
    )
    parser.add_argument(
        '--word',
        help='dircet check words'
    )
    parser.add_argument(
        '-',
        dest='stdin',
        action='store_true',
        help='source code from stdin'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help=argparse.SUPPRESS
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


r_equal_word = re.compile(r'^=([A-Za-z]+)$')
def get_equalword(s):
    m = r_equal_word.match(s)
    if m:
        return m.group(1)
    return None


def is_spell_diff_word(word1, word2):
    m = SequenceMatcher()
    m.set_seq2(word2)
    m.set_seq1(word1)
    check_a_e = True
    for tag, i1, i2, j1, j2 in m.get_opcodes():
        if tag == "replace":
            if (i1 != j1) or (i2 != j2):
                check_a_e = False
                break
            w1 = word1[i1:i2]
            w2 = word2[j1:j2]
            if not ((w1 == 'e' and w2 == 'a') or (w1 == 'a' and w2 == 'e')):
                check_a_e = False
                break
    if check_a_e:
        return True
    return False


r_glosbe_tag = re.compile('^\(([a-zA-Z,\s]*)\)(.*)')
def check_abbreviation_glosbe(word, d):
    if d['language'] == Glosbe.EN:
        text = d['text'].lower()
        # タグから除外
        m = r_glosbe_tag.match(text)
        if m:
            text = m.group(2).strip()
            for tag in m.group(1).split(','):
                if tag in ['online gaming', 'internet']:
                    return 10
                if tag in ['programing', 'computing']:
                    return 20
                elif tag in ['informal', 'colloquial abbreviation']:
                    desc = m.group(2).lower().strip()
                    if re.match('^(a\s|)' + word + '\w', desc):
                        return -5
        # 先頭の 'A ', 'An ' を取り除く
        if text.startswith('a '):
            text = text[2:]
        if text.startswith('an '):
            text = text[3:]
        # 末尾の . を削除
        text = text.rstrip('.')
        # 完全一致したら略語じゃない
        if text == word:
            return 2
        # 一単語のみの場合
        if len(text.split()) == 1:
            # ゴミ？
            if 'dust' == text:
                return -1
            # 前方一致した場合は略語と判定
            if text.startswith(word):
                diff = len(text) - len(word)
                # 過去形だったら略語じゃない
                if text[-2:] == 'ed' and diff < 3:
                    return 2
                return -5
        else:
            # XXX の略語って意味はダメ
            if text.startswith('abbreviation of'):
                if not text.startswith('abbreviation of ' + word + ' '):
                    return -5
            if text.startswith('abbreviation for'):
                if not text.startswith('abbreviation for ' + word + ' '):
                    return -5
            if text.startswith('short for'):
                if not text.startswith('short for ' + word + ' '):
                    return -5
            if text.startswith('short from for'):
                if not text.startswith('short from for ' + word + ' '):
                    return -5
            if text.startswith('shortened form of'):
                if not text.startswith('shortened form of ' + word + ' '):
                    return -5
            if text.startswith('clipped form of'):
                if not text.startswith('clipped form of ' + word + ' '):
                    return -5
            if text.startswith('alternative from of'):
                if not text.startswith('alternative from of ' + word + ' '):
                    return -5
    return 1


def check_abbreviation_glosbe_tuc(word, t):
    if 'meanings' in t:
        for meaning in t['meanings']:
            return check_abbreviation_glosbe(word, meaning)
    elif 'phrase' in t:
        return check_abbreviation_glosbe(word, t['phrase'])
    return 0


def get_abbreviation_glosbe_score(word, tuc):
    score = 0
    for t in tuc:
        rs = check_abbreviation_glosbe_tuc(word, t)
        score += rs
    return score


def has_glosbe_ja_meaings(t):
    if 'meanings' in t:
        for meaning in t['meanings']:
            if meaning['language'] == Glosbe.JA:
                return True
    return False


def check_suspicion_glosbe_impl(word):
    try:
        r = Glosbe.Translate(word, Glosbe.EN, Glosbe.JA)
        if r['result'] == 'ok':
            tuc = r['tuc']
            if len(tuc) == 0:
                return DictResult.NotFound

            has_ja = False
            # 辞書ごとのリストを作成する
            master_dicts = []
            optional_dicts = []
            for t in tuc:
                if has_glosbe_ja_meaings(t):
                    has_ja = True
                # 1,2736 の辞書だけ使う
                if any(x in [1, 2736, 91945] for x in t['authors']):
                    master_dicts.append(t)
                # それ以外の辞書のうち略語判定のみに使用
                elif any(x in [91945] for x in t['authors']):
                    optional_dicts.append(t)

            score = get_abbreviation_glosbe_score(word, master_dicts)
            if score < 0:
                add_abbreviation('glosbe', word)
                return DictResult.Abbreviation

            if not has_ja and score < 5:
                for t in optional_dicts:
                    if check_abbreviation_glosbe_tuc(word, t) < 0:
                        add_abbreviation('glosbe', word)
                        return DictResult.Abbreviation
            if len(master_dicts) > 0:
                add_cache('glosbe', word)
                return DictResult.Found
    except requests.HTTPError as e:
        print("Http error:", e.message)
        if e.response.status_code == 429:
            print("request count: ", Glosbe.count)
            print("Please access the glosbe, click the search button and check reCAPTCHA.")
            options.glosbe = False
            if options.debug:
                sys.exit(1)
        else:
            raise
    except:
        print("Unexpected error: \"{0}\" :".format(word), sys.exc_info()[0])
        raise
    return DictResult.NotFound


def check_suspicion_glosbe(word):
    # 2文字以下は略語かどうかの判別がつけにくいため除外
    if len(word) <= 2:
        return DictResult.NoCheck
    return check_suspicion_glosbe_impl(word)


def is_abbreviation_dejizo_word_impl(word, body):
    #if u'化学記号' in body:
    #    return True
    #if u'（…）' in body:
    #    return True
    # 英数と特定の記号のみなら略語とする
    # e.g. =refarence
    nbody = unicodedata.normalize('NFKC', body)
    eqword = get_equalword(nbody)
    if eqword:
        return not is_spell_diff_word(word, eqword.lower())
    if isalphasign(nbody):
        return True
    return False


def is_abbreviation_dejizo_impl(word, search_result, dict):
    titles = Dejizo.result_to_titles(search_result)
    if titles is None:
        return False
    for title in titles:
        # タイトルがすべて大文字だったら略語
        if Dejizo.get_title_text(title).isupper():
            return True
        r = Dejizo.get(title['ItemID'], dict)
        body = Dejizo.get_body(r).strip()
        if not is_abbreviation_dejizo_word_impl(word, body):
            return False
    return True


def check_suspicion_dejizo_impl(word, dict):
    try:
        r = Dejizo.search(word, dict)
        d = Dejizo.response_to_result(r)
        if d['ok'] and 'SearchDicItemResult' in d:
            result = d['SearchDicItemResult']
            count = int(result['ItemCount'])
            if count > 0:
                if len(word) > 4:
                    return DictResult.Found
                # 短い単語は詳細を get して調べる
                if Dejizo.is_getable(word, dict):
                    try:
                        if is_abbreviation_dejizo_impl(word, d, dict):
                            add_abbreviation('dejizo', word)
                            return DictResult.Abbreviation
                        else:
                            return DictResult.Found
                    except:
                        print("Unexpected error: " + word + " :" , sys.exc_info()[0])
                        pass
    except:
        pass
    return DictResult.NotFound


def check_suspicion_dejizo(word):
    # 2文字以下は略語かどうかの判別がつけにくいため除外
    if len(word) <= 2:
        return DictResult.NoCheck
    # どちらかの辞書に略語としてあったら即時 return
    ret = check_suspicion_dejizo_impl(word, Dejizo.DailyEJL)
    if ret == DictResult.Abbreviation:
        return DictResult.Abbreviation
    ret2 = check_suspicion_dejizo_impl(word, Dejizo.EJdict)
    if ret2 == DictResult.Abbreviation:
        return DictResult.Abbreviation
    # どちらの辞書にもなかったら return
    if ret == DictResult.NotFound and ret2 == DictResult.NotFound:
        return DictResult.NotFound
    # どちらかの辞書にあったらキャッシュに登録
    add_cache('dejizo', word)
    return DictResult.Found


def is_whitelist(word):
    if word in whitelist:
        return True
    if langkeywords and not options.disable_keywords:
        if word in langkeywords:
            return True
    # 辞書にあったら除外
    if word in gene:
        return True
    for cache in service_cache.values():
        if word in cache.gene:
            return True
    return False


r_past_ed = re.compile('.*[a-z]{2,2}ed$')
def is_suspicion_past(word, length):
    if length > 2 and word.endswith('ed'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if length > 3 and word.endswith('ied'):
            if is_whitelist(word[:-3] + 'y'):
                return False
        if r_past_ed.match(word):
            if is_whitelist(word[:-3]):
                return False
        if length > 4 and word.endswith('cked'):
            if is_whitelist(word[:-3]):
                return False
    return True


r_past_e = re.compile('.*[a-z]{2,2}en$')
def is_suspicion_past_participle(word, length):
    if length > 3+2 and word.endswith('en'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if r_past_e.match(word):
            if is_whitelist(word[:-3]):
                return False
            if is_whitelist(word[:-3] + 'e'):
                return False
    return True


r_post_er = re.compile('.*[a-z]{2,2}er$')
def is_suspicion_other_post_suffix(word, length):
    # er
    if length > 2 and word.endswith('er'):
        if is_whitelist(word[:-2]):
            return False
        if is_whitelist(word[:-1]):
            return False
        if length > 3 and word.endswith('ier'):
            if is_whitelist(word[:-3] + 'y'):
                return False
        if r_post_er.match(word):
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


r_ing = re.compile('.*[a-z]{2,2}ing$')
def is_suspicion_progressive(word, length):
    if length > 3 and word.endswith('ing'):
        if is_whitelist(word[:-3]):
            return False
        if is_whitelist(word[:-3] + 'e'):
            return False
        if r_ing.match(word):
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


def is_suspicion_post_suffix(word, length):
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
    # 他
    if not is_suspicion_other_post_suffix(word, length):
        return False
    return True


def is_suspicion_pre_suffix(word, length):
    # un
    if length > 2 and word.startswith('un'):
        if is_whitelist(word[2:]):
            return False
        elif not is_suspicion_post_suffix(word[2:], length-2):
            return False
    # re
    if length > 2 and word.startswith('re'):
        if is_whitelist(word[2:]):
            return False
        elif not is_suspicion_post_suffix(word[2:], length-2):
            return False
    return True


def check_suspicion(word):
    length = len(word)
    # 1文字だけは除外
    if length <= 1:
        return DictResult.NoCheck
    if not isalpha(word):
        return DictResult.NoCheck
    if is_whitelist(word):
        return DictResult.Found
    # 略語リストにあったら即アウト
    for cache in service_cache.values():
        if word in cache.abbreviations:
            return DictResult.Abbreviation
    # 接尾辞
    if not is_suspicion_post_suffix(word, length):
        return DictResult.Found
    # 接頭辞
    if not is_suspicion_pre_suffix(word, length):
        return DictResult.Found
    # Web API
    if options.glosbe:
        r = check_suspicion_glosbe(word)
        if r != DictResult.NotFound:
            return r
    if options.dejizo:
        r = check_suspicion_dejizo(word)
        if r != DictResult.NotFound:
            return r
    return DictResult.NotFound


r_sign = re.compile('[!-/:-@[-`{-~]')
r_transform  = re.compile('([a-z0-9])([A-Z])(?=[A-Z]*[a-z\s]|$)')
r_transform2 = re.compile('(\s[A-Z])([A-Z])(?=[a-z])')
def text_transform(text):
    text = re.sub(r_sign, ' ', text)
    text = re.sub(r_transform , lambda x: x.group(1) + " " + x.group(2), text)
    text = re.sub(r_transform2, lambda x: x.group(1) + " " + x.group(2), text)
    return text


def checkword(word, filepath, line, detected_words):
    global words
    global checked_words
    if not word in checked_words:
        location = Location(filepath, line)
        if words.has_key(word):
            words[word].add_location(location)
            detected_words.append({word: location})
        else:
            result = check_suspicion(word)
            if DictResult.is_suspicion(result):
                words[word] = WordResult(result, location)
                detected_words.append({word: location})
            else:
                checked_words.append(word)


def checktagger(filepath, text, line):
    detected_words = []
    tags_plain = tagger.TagText(text)
    tags = treetaggerwrapper.make_tags(tags_plain)
    for tag in tags:
        if isinstance(tag, treetaggerwrapper.NotTag):
            continue
        word = tag.word.lower()
        checkword(word, filepath, line, detected_words)
    return detected_words


def checksplit(filepath, text, line):
    global words
    global checked_words
    detected_words = []
    for tag in text.split():
        word = tag.lower()
        checkword(word, filepath, line, detected_words)
    return detected_words


def detect_encoding(path):
    global default_encoding
    global prev_detect_encoding
    global default_encoding_change_count
    encoding_list = [ 'utf-8', 'utf-8-sig', 'shift_jis', 'euc_jp' ]
    encoding_list.remove(default_encoding)
    encoding_list.insert(0, default_encoding)
    for encoding in encoding_list:
        f = codecs.open(path, 'r', encoding=encoding)
        try:
            f.readline()
            f.close()
            if encoding == prev_detect_encoding:
                default_encoding_change_count += 1
                if default_encoding_change_count >= 3:
                    default_encoding = encoding
                else:
                    default_encoding_change_count = 0
            else:
                prev_detect_encoding = encoding
            return encoding
        except:
            f.close()
    return default_encoding


r_system_include = re.compile(r'^\s*#\s*include\s*<.*>')
def ischeckline(lang, line):
    if len(line) > 0:
        if lang == 'c++':
            if r_system_include.match(line):
                return False
        return True
    return False


def check(f, report_in_line):
    global langkeywords
    filepath = f.getpath()
    filesize = f.getsize()
    lang = f.getlanguage()
    line_count = 1
    line = f.readline()
    while line:
        rstrip_line = line.rstrip()
        if report_in_line:
            print(f.getrawline().rstrip())
        langkeywords = f.getkeywords()
        text = line.strip()
        if len(text) > 0:
            if ischeckline(lang, line):
                if tagger is None:
                    detected_words = checksplit(filepath, text_transform(text), line_count)
                else:
                    detected_words = checktagger(filepath, text_transform(text), line_count)
                if report_in_line:
                    for d in detected_words:
                        for word in d.keys():
                            print("warning: \"{0}\": is ok ??".format(word))
        line_count += 1
        line = f.readline()
        if options.progress and not report_in_line:
            pos = f.tell()
            sys.stdout.write('{0:.2f}%'.format(pos*100.0/filesize)+ '\r')
    f.close()

def get_print_path(location):
    if options.relpath:
        return location.relpath
    else:
        return location.file


def make_base_message(location, k):
    return "{0}({1}): warning: \"{2}\"".format(get_print_path(location), location.line, k)

def printresult():
    if options.list_all:
        for k,v in sorted(words.items(), key=lambda x: len(x[1])):
            r = v.result
            for location in v.locations:
                if r == DictResult.Abbreviation:
                    print("{0}: is abbreviation".format(make_base_message(location, k)))
                else:
                    print("{0}: is ok ??".format(make_base_message(location, k)))
    else:
        for k,v in sorted(words.items(), key=lambda x: x[0]):
            r = v.result
            location = v.locations[0]
            if r == DictResult.Abbreviation:
                msg = "{0}: is abbreviation".format(make_base_message(location, k))
            else:
                msg = "{0}: is ok ??".format(make_base_message(location, k))
            if len(v.locations) > 1:
                print("{0} ({1})".format(msg, len(v.locations)))
            else:
                print(msg)
        print("Total number detected: {0}".format(len(words)))


def checkfile(filepath):
    filename = os.path.basename(filepath)
    encoding = options.encoding
    if encoding is None:
        encoding = detect_encoding(filepath)
    f = filereader.OpenFile(filepath, encoding=encoding, language=options.language)
    print('check: {0}'.format(filename))
    check(f, False)


def checkdir(dir):
    prev = Location.current_path
    Location.current_path = dir
    for d in os.listdir(dir):
        d = os.path.join(dir, d)
        if os.path.isdir(d):
            basename = os.path.basename(d)
            if basename not in exclude_dir:
                print(">>>> Entering directory {0}".format(basename))
                checkdir(d)
                print("<<<< Leaving  directory {0}".format(basename))
        else:
            if not re.match(options.extension, os.path.splitext(d)[1].strip('.')):
                print('skip: {0}: not match extension [{1}]'.format(d, options.extension))
            else:
                checkfile(d)
    Location.current_path = prev


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


def setup_cache_rebuild():
    files = Cache.get_files(options.cache_dir, options.cache_rebuild)
    options.file = []
    locked = Cache.islock(options.cache_dir, options.cache_rebuild)
    Cache.lock(options.cache_dir, options.cache_rebuild)
    for f in files:
        lockfile = f + '.lock'
        options.file.append(lockfile)
        if not locked:
            os.remove(f)
    options.cache = True
    setattr(options, options.cache_rebuild, True)


def setup():
    global gene
    global whitelist
    global abbreviations
    if options.cache_dir is None:
        options.cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    if options.cache_rebuild:
        setup_cache_rebuild()
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
        for name in cache_choices:
            if getattr(options, name):
                setup_cache(name)
    if options.exclude:
        for e in options.exclude:
            whitelist.extend(e.split(','))
    if options.load_cache:
        for f in options.load_cache:
            whitelist.extend(make_wordlist(Cache.get_gene_filename(options.cache_dir, f)))
            abbreviations.extend(make_wordlist(Cache.get_abbreviation_filename(options.cache_dir, f)))
    if options.safe_mode:
        Glosbe.set_safe_mode(True)
    if options.no_request_limit:
        Glosbe.set_safe_mode(False)


def checkfilelist():
    if not options.file:
        return
    for f in options.file:
        if os.path.isdir(f):
            checkdir(f)
        else:
            checkfile(f)
    print('==== begin ====')
    printresult()
    print('====  end  ====')


def checkstdin():
    encoding = options.encoding
    f = filereader.OpenStdin(encoding=encoding, language=options.language)
    check(f, True)


def checkdirect(text):
    encoding = options.encoding
    f = filereader.OpenText(text, encoding=encoding, language=options.language)
    check(f, True)


def main():
    global options
    options, parser = parse_command_line()
    setup()
    if options.word:
        checkdirect(options.word)
    elif options.stdin:
        checkstdin()
    else:
        if options.file is None or len(options.file) <= 0:
            parser.print_help()
        else:
            checkfilelist()
    if options.cache_rebuild:
        Cache.unlock(options.cache_dir, options.cache_rebuild)


if __name__ == '__main__':
    main()
