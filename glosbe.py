#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import pprint

class Glosbe:
    EN = 'en'
    JA = 'ja'
    English = EN
    Japanese = JA

    api_url = 'https://glosbe.com/gapi/translate'

    def __init__(self):
        self.src = Glosbe.EN
        self.dst = Glosbe.JA

    def set_from_lang(self, lang):
        self.src = lang

    def set_to_lang(self, lang):
        self.dst = lang

    def translate(self, phrase):
        return Glosbe.translate(phrase, self.src, self.dst)

    @staticmethod
    def translate(phrase, from_lang, to_lang):
        payload = { 
            'from' : from_lang,
            'dest' : to_lang,
            'format' : 'json',
            'phrase' : phrase,
            'pretty' : 'true'
        }
        r = requests.get(Glosbe.api_url, params=payload)
        r.raise_for_status()
        return r.json()


if __name__ == '__main__':
    glosbe = Glosbe()
    if len(sys.argv) > 1:
        r = Glosbe.translate(sys.argv[1], Glosbe.EN, Glosbe.JA)
    else:
        r = Glosbe.translate('test', Glosbe.EN, Glosbe.JA)
    pprint.pprint(r)
