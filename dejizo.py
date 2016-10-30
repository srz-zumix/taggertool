#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import pprint

from xml.etree import ElementTree

def etree_to_dict(t):
    def tag_name(t):
        if '}' in t.tag:
            return t.tag.split('}')[1]
        else:
            return t.tag

    def etree_to_dict_i(t):
        d = {}
        children = list(t)
        if len(children) > 0:
            dd = {}
            for c in children:
                name = tag_name(c)
                cd = etree_to_dict_i(c)
                if name in dd:
                    if isinstance(dd[name], list):
                        dd[name].append(cd)
                    else:
                        da = [ dd[name], cd ]
                        dd[name] = da 
                else:
                    dd[name] = cd
            d.update(dd)
        else:
            return t.text
        return d

    d = {}
    d[tag_name(t)] =etree_to_dict_i(t)
    return d


class Dejizo:
    api_url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'
    EJdict = 'EJdict'
    DailyEJL = 'DailyEJL'

    def __init__(self):
        pass

    @staticmethod
    def search(phrase, dic):
        payload = { 
            'Dic' : dic,
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
        result.update(etree_to_dict(tree))
        return result


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 1:
        r = Dejizo.search(sys.argv[1], Dejizo.EJdict)
    else:
        r = Dejizo.search('test', Dejizo.EJdict)
    print(r.content)
    pprint.pprint(Dejizo.response_to_result(r))
