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
    def is_getable(phrase, dic):
        if dic == Dejizo.DailyEJL:
            if phrase[0] != 'a' and phrase != 'A':
                return False
        return True

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
    def result_to_titles(result):
        ids = []
        if result['ok'] and 'SearchDicItemResult' in result:
            titlelist_parent = result['SearchDicItemResult']['TitleList']
            if titlelist_parent:
                titlelist = titlelist_parent['DicItemTitle']
                if isinstance(titlelist, list):
                    return titlelist
                else:
                    return [titlelist]
        return None

    @staticmethod
    def get_title_text(dicTitle):
        if 'Title' in dicTitle:
            r = dicTitle['Title']
            while isinstance(r, dict):
                r = r.values()[0]
            return r
        return None

    @staticmethod
    def response_to_result(response):
        if not response.ok:
            return { 'ok' : False, 'status_code': response.status_code }
        tree = ElementTree.fromstring(response.content)
        result = { 'ok' : True, 'status_code': response.status_code }
        result.update(etree_to_dict(tree))
        return result

    @staticmethod
    def get_body_from_result(result):
        if result['ok'] and 'GetDicItemResult' in result:
            r = result['GetDicItemResult']
            try:
                return r['Body']['div']['div']
            except:
                pass
            try:
                return r['Body']['div']
            except:
                pass
        return None

    @staticmethod
    def get_body(response):
        if not response.ok:
            return None
        tree = ElementTree.fromstring(response.content)
        ns = { 'ns' : 'http://btonic.est.co.jp/NetDic/NetDicV09' }
        body = tree.find('.//ns:Body', namespaces=ns)
        def innertext(tag):
            return (tag.text or '') + ''.join(innertext(e) for e in tag) + (tag.tail or '')
        return innertext(body)


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    dic = Dejizo.EJdict
    phrase = 'test'
    if len(sys.argv) > 2:
        dic = sys.argv[2]
    if len(sys.argv) > 1:
        phrase = sys.argv[1]
    def dejizo(phrase, dic):
        r = Dejizo.search(phrase, dic)
        print(r.content)
        d = Dejizo.response_to_result(r)
        pprint.pprint(d)
        ids = Dejizo.result_to_ids(d)
        print(ids)
        if Dejizo.is_getable(phrase, dic):
            for id in ids:
                gr = Dejizo.get(id, dic)
                print(gr.content)
                print(Dejizo.get_body(gr))
        if len(ids) > 0:
            return True
        return False
    if not dejizo(phrase, dic):
        if dic == Dejizo.DailyEJL:
            dejizo(phrase, Dejizo.EJdict)
        else:
            dejizo(phrase, Dejizo.DailyEJL)
