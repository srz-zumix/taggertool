import unittest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import abbreviation
from abbreviation import DictResult


class Test_glosbe(unittest.TestCase):
    def test_apple(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('apple'))

    def test_again(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('again'))

#    def test_they(self):
#        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('they'))

    def test_their(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('their'))

    # test \u2019
    def test_your(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('your'))

    # test \u014b
    def test_eng(self):
        self.assertEqual(DictResult.NotFound, abbreviation.check_suspicion_glosbe('eng'))

    # test \uxf6
    def test_zoa(self):
        self.assertEqual(DictResult.NotFound, abbreviation.check_suspicion_glosbe('zoa'))

    def test_tramp(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('tramp'))

    # socore adjust
    def test_topic(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('topic'))

    # neew 2 word check
    def test_pub(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe('pub'))

    # archaic
    def test_vert(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe('vert'))

    def test_ops(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe('ops'))

    def test_cgs(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe('cgs'))

    def test_what(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('what'))

    def test_found(self):
        words = [
            'acorn',
            'allocation',
            'begin',
            'block',
            'compliment',
            'celsius',
            'kana',
            'pat',
            'posit',
            'pythagoras',
            'repository',
            'role',
            'rule',
            'runtime',
            'stage',
            'team',
            'teardown',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)

    def test_abbreviation(self):
        words = [
            'abs',
            'chk',
            'min',
            'max',
            'neg',
            'par',
            'sec',
            'seg',
            'sig',
            'semi',
            'vid',
            ]
        for word in words:
            self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe(word), word)

    def test_found_else(self):
        words = [
            'gis',
            'pos',
            ]
        for word in words:
            self.assertNotEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)

    def test_notfound(self):
        words = [
            'bailouts',
            ]
        for word in words:
            self.assertNotEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)

    # need plural word search check
    def test_plural(self):
        words = [
            'zos',
            ]
        for word in words:
            self.assertEqual(DictResult.NotFound, abbreviation.check_suspicion_glosbe(word), word)

    # gen'eration's
    def test_plural_abbreviation(self):
        words = [
            'certs',
            'gens',
            'subs',
            ]
        for word in words:
            self.assertEqual(DictResult.Abbreviation, abbreviation.check_suspicion_glosbe(word), word)

    def test_abbreviation_or_notfound(self):
        words = [
            'pos',
            ]
        for word in words:
            r = abbreviation.check_suspicion_glosbe(word)
            self.assertIn(r, [ DictResult.Abbreviation, DictResult.NotFound ], word)

    def test_misspelling(self):
        words = [
            'usefull',
            'extention',
            'repetetive',
            ]
        for word in words:
            self.assertEqual(DictResult.Misspelling, abbreviation.check_suspicion_glosbe(word), word)

    def test_2736(self):
        words = [
            'cannot',
            'disallow',
            'insensitive',
            'mathematical',
            'progress',
            'resume',
            'subject',
            'useful',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)


if __name__ == '__main__':
    unittest.main()
