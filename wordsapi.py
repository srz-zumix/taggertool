#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
#import codecs
import pprint

class WordsApi:
    api_url = 'https://wordsapiv1.p.mashape.com/words/'

    def __init__(self):
        pass

    @staticmethod
    def Definitions(phrase):
        r = requests.get(WordsApi.api_url + phrase + '/definitions')
        return r.json()


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 1:
        r = WordsApi.Definitions(sys.argv[1])
    else:
        r = WordsApi.Definitions('test')
    pprint.pprint(r)
