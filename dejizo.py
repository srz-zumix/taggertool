#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import pprint

from xml.etree import ElementTree

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
            'Prof' : 'XHTML',
            'PageSize' : 20,
            'PageIndex' : 0
        }
        r = requests.get(Dejizo.api_url, params=payload)
        r.raise_for_status()
        return r
        
    @staticmethod
    def response_to_result(response):
        if not response.ok:
            return { 'ok' : False, 'status_code': response.status_code }
        tree = ElementTree.fromstring(response.content)
        result = { 'ok' : True, 'status_code': response.status_code }
        for elem in tree.getiterator():
            if '}' in elem.tag:
                result[elem.tag.split('}')[1]] = elem.text
            else:
                result[elem.tag] = elem.text
        return result


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 1:
        r = Dejizo.search(sys.argv[1])
    else:
        r = Dejizo.search('test')
    print r.text
