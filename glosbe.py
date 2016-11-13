﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
#import codecs
import pprint

class Glosbe:
    EN = 'en'
    JA = 'ja'
    English = EN
    Japanese = JA

    count = 0

    api_url = 'https://glosbe.com/gapi/translate'

    def __init__(self):
        self.src = Glosbe.EN
        self.dst = Glosbe.JA

    def set_from_lang(self, lang):
        self.src = lang

    def set_to_lang(self, lang):
        self.dst = lang

    def translate(self, phrase):
        return Glosbe.Translate(phrase, self.src, self.dst)

    def get_meanings(self, response):
        return Glosbe.GetMeanings(response, self.dst)

    def get_phrases(self, response):
        return Glosbe.GetPhrases(response, self.dst)

    @staticmethod
    def GetMeanings(response, to_lang):
        words = u''
        for r in response['tuc']:
            if 'meanings' in r:
                for m in r['meanings']:
                    if m['language'] == to_lang:
                        if len(words) > 0:
                            words += u','
                        words += m['text']
        return words

    @staticmethod
    def GetPhrases(response, to_lang):
        words = ''
        for r in response['tuc']:
            if 'phrase' in r:
                phrase = r['phrase']
                if phrase['language'] == to_lang:
                    if len(words) > 0:
                        words += ','
                    words += phrase['text']
        return words

    @staticmethod
    def Translate(phrase, from_lang, to_lang):
        payload = { 
            'from' : from_lang,
            'dest' : to_lang,
            'format' : 'json',
            'phrase' : phrase,
            'pretty' : 'true'
        }
        Glosbe.count += 1
        r = requests.get(Glosbe.api_url, params=payload)
        r.raise_for_status()
        return r.json()


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    g = Glosbe()
    if len(sys.argv) > 1:
        r = g.translate(sys.argv[1])
    else:
        r = g.translate('test')
    #pprint.pprint(r)
    print g.get_meanings(r)
    print g.get_phrases(r)