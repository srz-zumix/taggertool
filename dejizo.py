#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import pprint
import codecs

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
    api_search_url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'
    api_getitem_url = 'http://public.dejizo.jp/NetDicV09.asmx/GetDicItemLite'
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
        r = requests.get(Dejizo.api_search_url, params=payload)
        r.raise_for_status()
        return r

    @staticmethod
    def get(id, dic):
        payload = { 
            'Dic' : dic,
            'Item' : id,
            'Prof' : 'XHTML',
            'Loc' : '',
        }
        r = requests.get(Dejizo.api_getitem_url, params=payload)
        r.raise_for_status()
        return r

    @staticmethod
    def result_to_ids(result):
        ids = []
        if result['ok'] and 'SearchDicItemResult' in result:
            titlelist = result['SearchDicItemResult']['TitleList']
            if titlelist:
                title = titlelist['DicItemTitle']
                if isinstance(title, list):
                    for item in title:
                        ids.append(item['ItemID'])
                else:
                    ids.append(title['ItemID'])
        return ids

    @staticmethod
    def response_to_result(response):
        if not response.ok:
            return { 'ok' : False, 'status_code': response.status_code }
        tree = ElementTree.fromstring(response.content)
        result = { 'ok' : True, 'status_code': response.status_code }
        result.update(etree_to_dict(tree))
        return result

    @staticmethod
    def get_body(result):
        if result['ok'] and 'GetDicItemResult' in result:
            r = result['GetDicItemResult']
            try:
                return r['Body']['div']['div']
            except:
                pass
        return None


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 2:
        r = Dejizo.search(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        r = Dejizo.search(sys.argv[1], Dejizo.EJdict)
    else:
        r = Dejizo.search('test', Dejizo.EJdict)
    print(r.content)
    d = Dejizo.response_to_result(r)
    pprint.pprint(d)
    ids = Dejizo.result_to_ids(d)
    print(ids)
    for id in ids:
        gr = Dejizo.get(id, Dejizo.EJdict)
        print(gr.content)
        dd = Dejizo.response_to_result(gr)
        pprint.pprint(dd)
        print(Dejizo.get_body(dd))
