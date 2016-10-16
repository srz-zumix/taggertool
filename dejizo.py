#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import pprint

class Dejizo:
    api_url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'

    def __init__(self):
        pass

    @staticmethod
    def search(phrase):
        payload = { 
            'Dic' : 'EJdict',
            'Word' : phrase,
            'Scope' : 'HEADWORD',
            'Match' : 'EXACT',
            'Merge' : 'AND',
            'Prof' : 'JSON',
            'PageSize' : 1,
            'PageIndex' : 0
        }
        r = requests.get(Dejizo.api_url, params=payload)
        r.raise_for_status()
        return r


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 1:
        r = Dejizo.search(sys.argv[1])
    else:
        r = Dejizo.search('test')
    pprint.pprint(r)
