#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import requests

from glosbe import Glosbe
from abbreviation_cache import cache
from abbreviation_defs import DictResult
from abbreviation_defs import WordResult
from abbreviation_defs import MisspellingError
from abbreviation_defs import IgnoreError
from abbreviation_defs import InflectedError
from abbreviation_defs import PluralError
from abbreviation_defs import PastError
from abbreviation_defs import RequestLimitError

_checked_inflected = []

_global_ignore_list = [
    'tsk',
    'tut',
    ]

def isascii(s):
    if s:
        return max([ord(char) for char in s]) < 128


_r_html_special_char = re.compile('&[#|\w]+;')
_r_an = re.compile('^(a|an)\s', re.IGNORECASE)
_r_remove_tag = re.compile('[<|\[](/|)(i|b|sup)[>|\]]', re.IGNORECASE)
def _normalize_dict_text(text):
    # タグを削除
    text = _r_remove_tag.sub('', text)
    # html 特殊文字削除
    text = _r_html_special_char.sub('', text)
    # 先頭の 'A ', 'An ' を取り除く
    text = _r_an.sub('', text)
    # \u2019 (right single quartation) replact
    text = text.replace(r'\u2019', '\'')
    # 末尾の . ; を削除
    text = text.rstrip('.;')
    # ; 以降は除外
    #text = text.split(';')[0]
    return text


def _check_all_initials(word, text):
    split_texts = text.split()
    if not len(word) == len(split_texts):
        return False
    for i in range(0, len(word)):
        if not word[i] == split_texts[i][0]:
            return False
    return True


_r_glosbe_tag = re.compile('^\(([a-zA-Z,\s]*)\)(.*)')
#_r_cockney_slang = re.compile('.*slang.*\[from [0-9]+th c\.\].*')
_r_slang = re.compile('^(|.*[^A-Za-z])slang[^A-Za-z].*')
def _check_en(word, d, adict, optional):
    text = d['text']
    # タグから除外
    m = _r_glosbe_tag.match(text)
    tags = []
    if m:
        text = m.group(2).strip()
        tags = m.group(1).lower().split(',')

    origin_case_text = _normalize_dict_text(text)
    text = origin_case_text.lower()
    # 同一文はチェックしない
    if text in adict:
        return 0
    # 整形したテキストを保存しておく
    if not optional:
        adict.append(text)

    find_value = 1

    # 不適切な言葉は点数下げる
    if 'sex' == text:
        return -10

    # タグをチェック
    for tag in tags:
        tag = tag.strip()
        if tag in ['online gaming', 'internet']:
            find_value = 3
        if tag in ['programing', 'computing']:
            return 20
        if tag in ['informal', 'colloquial abbreviation']:
            desc = m.group(2).lower().strip()
            if re.match('^(a\s|)' + word + '\w', desc):
                return -5
        if tag in ['colloquial']:
            find_value = 0
        if tag in ['chiefly us', 'chiefly uk']:
            raise IgnoreError
        if tag in ['obsolete', 'cockney rhyming slang', 'slang', 'nonstandard', 'archaic', 'mostly uncountable']:
            # スラング or すたれた ものは除外
            raise IgnoreError
        if tag in ['of champagne', 'golf', 'anthropology', 'music', 'baseball', 'zoology', 'french']:
            # その他、品種で除外
            raise IgnoreError
    # cockney rhyming slang
#    if _r_cockney_slang.match(text):
#        raise IgnoreError
    if _r_slang.match(text):
        raise IgnoreError
    if text.startswith('spanish,'):
        raise IgnoreError
    if text.startswith('roman alphabet'):
        raise IgnoreError

    # ゴミ？
    if 'dust' == text:
        return -1

    def check_one_word(text):
        # 完全一致したら略語じゃない
        if text == word:
            return DictResult.Found
        # 前方一致した場合は略語と判定
        if text.startswith(word):
            diff = len(text) - len(word)
            # 過去形だったら略語じゃない
            if text[-2:] == 'ed' and diff < 3:
                return DictResult.Found
            # 形容詞だったら略語じゃない
            if text[-2:] == 'ly' and diff == 2:
                return DictResult.Found
            return DictResult.Abbreviation
        # 
        if len(word) < 4:
            if word in text:
                return DictResult.Abbreviation
        # 複数系の確認
        if text[-1:] == 's' and word[-1:] == 's':
            if text.startswith(word[:-1]):
                return DictResult.Abbreviation
        return DictResult.NotFound

    split_texts = re.split('\s|-', text, 3)
    # 1 or 2単語のみの場合
    if len(split_texts) <= 2:
        for oneword in split_texts:
            r = check_one_word(oneword)
            if r == DictResult.Found:
                return find_value * 2
            elif r == DictResult.Abbreviation:
                return -4
    else:
        # Abbreviation
        def check_short_of(starts):
            if text.startswith(starts):
                if ',' in text:
                    first = text.split(',')[0]
                    if any([s.startswith(first) for s in adict[:-1]]):
                        # , を除いたテキストがあったら除外する
                        raise IgnoreError
                after = text[len(starts):]
                after_words = re.split(',|:', after)[0].split()
                if len(after_words) == 1:
                    return True
                else:
                    # 文中に word がない場合は略語と判定
                    if word not in after_words:
                        return True
            return False

        short_of_starts = [
            'abbreviation of',
            'abbreviation for',
            'abbreviated form of',
            'short for',
            'short from for',
            'short form of',
            'shortened form of',
            'clipped form of',
        ]
        for ss in short_of_starts:
            if check_short_of(ss):
                return -5

        eye_dialect_of_starts = [
            'eye dialect spelling of',
        ]
        for ss in eye_dialect_of_starts:
            if check_short_of(ss):
                if optional:
                    return -3
                else:
                    return -5

        # misspelling
        def check_misspelling_of(starts):
            if text.startswith(starts):
                after = text[len(starts):]
                after_words = re.split(',|:\-', after)[0].split()
                join_text = ''.join(after_words)
                # 連結して word と一致する場合はスペルミスと判断しない
                if join_text != word:
                    return True
                if '\'' in join_text:
                    join_text = join_text.replace('\'', '')
                    if join_text.startswith(word):
                        return True
            return False

        if check_misspelling_of('misspelling of'):
            raise MisspellingError

        # Alternative
        def check_alternative_of(starts, check_join):
            if text.startswith(starts):
                if check_join:
                    after = origin_case_text[len(starts):]
                    after_words = re.split('\s|\-', re.split(',|:', after)[0])
                    join_text = ''.join(after_words)
                    if join_text == word:
                        return False
                r_case = re.compile(starts + '\s*(\w*)', re.IGNORECASE)
                m = r_case.match(origin_case_text)
                if m:
                    if m.group(1).isupper():
                        return True
                    else:
                        raise InflectedError(m.group(1))
            return False

        alternative_of_starts = [
            'alternative from of',
            'alternative form of',
            'alternative spelling of',
        ]
        alternative_of_starts2 = [
            'alternative letter-case form of',
        ]
        for ss in alternative_of_starts:
            if check_alternative_of(ss, True):
                return -2
        for ss in alternative_of_starts2:
            if check_alternative_of(ss, False):
                return -2

        ignore_starts = [
            'obsolete spelling of',
            'obsolete form of',
            'currency of',
            'the currency of',
            'the basic unit of money in',
            'name of the letter',
            'something shaped like the letter',
            'the name of the Latin script letter',
            'plant, member of',
            'expression of',
            'pet form of',
            'common nickname for',
        ]
        for ss in ignore_starts:
            if text.startswith(ss):
                raise IgnoreError

        if 'sound of' in text:
            raise IgnoreError

        # Individual correspondence (has)
        if 'indicative form of' in text:
            return 3

        # inflected
        def check_inflected_of(starts):
            if text.startswith(starts):
                after = text[len(starts):]
                after_words = re.split(',|:', after)[0].split()
                if len(after_words) == 1:
                    return after_words[0]
                else:
                    raise IgnoreError
            return None

        # past
        past_of_starts = [
            'simple past of',
            'simple past tense of',
            'past participle of',
        ]
        for ss in past_of_starts:
            x = check_inflected_of(ss)
            if x:
                raise PastError(x)

        # plural
        plural_of_starts = [
            'plural of',
            'plural form of',
            'singular form of',
        ]
        for ss in plural_of_starts:
            x = check_inflected_of(ss)
            if x:
                raise PluralError(x)

        # ; 区切りで単語チェック
        for t in text.split(';'):
            if len(t.split()) == 1:
                r = check_one_word(t)
                if r == DictResult.Found:
                    return find_value * 2
                elif r == DictResult.Abbreviation:
                    return -4
        # 
        if _check_all_initials(word, text):
            return -5

    return find_value


def _check_meaning(word, d, adict, optional):
    if d['language'] == Glosbe.EN:
        return _check_en(word, d, adict, optional)
    elif d['language'] == Glosbe.JA:
        return 2
    return 0


def _check_tuc(word, t, adict, optional):
    if 'meanings' in t:
        score = 0
        for meaning in t['meanings']:
            score += _check_meaning(word, meaning, adict, optional)
        return score
    elif 'phrase' in t:
        return _check_meaning(word, t['phrase'], adict, optional)
    return 0


def _get_score(word, tuc, optional_tuc, inflected):
    score = 0
    misspelling = False
    adict = []
    for t in tuc[:]:
        try:
            rs = _check_tuc(word, t, adict, False)
            score += rs
        except IgnoreError:
            tuc.remove(t)
        except InflectedError as e:
            tuc.remove(t)
            if e.message not in inflected:
                inflected.append(e)
        except MisspellingError:
            misspelling = True
            tuc.remove(t)
        except:
            raise
    for t in optional_tuc:
        try:
            rs = _check_tuc(word, t, adict, True)
            if rs < 0:
                score += rs
        except IgnoreError:
            pass
        except InflectedError as e:
            if e.message not in inflected:
                inflected.append(e)
        except MisspellingError:
            misspelling = True
        except:
            raise
    return score, misspelling


def _has_ja_meaings_or_phrase(t):
    if 'meanings' in t:
        for meaning in t['meanings']:
            if meaning['language'] == Glosbe.JA:
                return True
    if 'phrase' in t:
        if t['phrase']['language'] == Glosbe.JA:
            return True
    return False


def _check_suspicion_impl(word, translate_word=None):
    check_case = False
    if not isascii(word):
        return DictResult.NoCheck
    if word in _global_ignore_list:
        return DictResult.NoCheck
    if translate_word is None:
        check_case = True
        translate_word = word
    r = Glosbe.Translate(translate_word, Glosbe.EN, Glosbe.JA)
    if r['result'] == 'ok':
        tuc = r['tuc']
        if len(tuc) == 0:
            return DictResult.NotFound

        ja_count = 0
        # 辞書ごとのリストを作成する
        master_dicts = []
        optional_dicts = []
        for t in tuc:
            if _has_ja_meaings_or_phrase(t):
                ja_count += 1
            # 信頼する辞書だけ使う
            if any(x in [1, 84, 93369] for x in t['authors']):
                master_dicts.append(t)
            # それ以外の辞書のうち略語判定のみに使用
            elif any(x in [91945] for x in t['authors']):
                optional_dicts.append(t)

        global _checked_inflected
        inflected_list = []
        score, misspelling = _get_score(word, master_dicts, optional_dicts, inflected_list)
        _checked_inflected.append(word)
        inflected_found = []
        for e in inflected_list:
            inflected_word = e.message
            if inflected_word in inflected_found:
                score += 1
            if inflected_word in _checked_inflected:
                continue
            result = _check_suspicion(inflected_word)
            if result == DictResult.Abbreviation:
                if isinstance(e, PluralError) and inflected_word + 's' == word:
                    return DictResult.Abbreviation
                else:
                    score -= 5
            elif result == DictResult.Found:
                if isinstance(e, PluralError):
                    if inflected_word + 's' == word:
                        return DictResult.Found
                    else:
                        score += 1
                if isinstance(e, PastError):
                    if inflected_word + 'ed' == word or inflected_word[:-1] + 'ed' == word:
                        return DictResult.Found
                    else:
                        score += 3
                inflected_found .append(inflected_word)
            elif result == DictResult.NotFound:
                pass
            elif result == DictResult.NoCheck:
                pass
            else:
                score -= 3
        score += (int)(ja_count / 10)
        if score < 0:
            cache.add_abbreviation('glosbe', word)
            return DictResult.Abbreviation

        if misspelling and score < 2:
            return DictResult.Misspelling

        threshold_score = 0
        threshold_tuc_count = 20
        if len(word) <= 3:
            threshold_score = 2
            threshold_tuc_count = 30
        elif len(word) <= 4:
            threshold_score = 1
            threshold_tuc_count = 25
        if score > threshold_score:
            cache.add_cache('glosbe', word)
            return DictResult.Found
        if len(tuc) > threshold_tuc_count:
            cache.add_cache('glosbe', word)
            return DictResult.Found

        if ja_count > 0 and check_case:
            # case sensitive なので先頭を大文字にしてリトライ
            return _check_suspicion_impl(word, (word[0]).upper() + word[1:])
    return DictResult.NotFound


def _check_suspicion(word):
    try:
        return _check_suspicion_impl(word)
    except requests.HTTPError as e:
        print("Http error:", e.message)
        if e.response.status_code == 429:
            print("request count: ", Glosbe.count)
            print("Please access the glosbe, click the search button and check reCAPTCHA.")
            raise RequestLimitError
        else:
            raise
    except:
        print("Unexpected error: \"{0}\" :".format(word), sys.exc_info()[0])
        raise
    return DictResult.NotFound


def check_suspicion(word):
    # 2文字以下は略語かどうかの判別がつけにくいため除外
    if len(word) <= 2:
        return DictResult.NoCheck
    result = _check_suspicion(word)
    global _checked_inflected
    _checked_inflected = []
    return result
