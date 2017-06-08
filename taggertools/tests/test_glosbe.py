import unittest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import abbreviation_glosbe
from abbreviation_defs import DictResult


class Test_glosbe(unittest.TestCase):
    def test_apple(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('apple'))

    def test_again(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('again'))

#    def test_they(self):
#        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('they'))

    def test_their(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('their'))

    # test \u2019
    def test_your(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('your'))

    # test \u014b
    def test_eng(self):
        self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion('eng'))

    # test \uxf6
    def test_zoa(self):
        self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion('zoa'))

    def test_tramp(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('tramp'))

    # socore adjust
    def test_topic(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('topic'))

    # neew 2 word check
    def test_pub(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion('pub'))

    # archaic
    def test_vert(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion('vert'))

    def test_ops(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion('ops'))

    def test_cgs(self):
        self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion('cgs'))

    def test_what(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('what'))

    def test_filesystem(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('filesystem'))

    def test_righthand(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('righthand'))

    def test_they(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('they'))

    def test_did(self):
        self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion('did'))

    def test_non(self):
        self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion('non'))

    def test_lev(self):
        self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion('lev'))

    def test_cee(self):
        self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion('cee'))

    def test_tsk(self):
        self.assertEqual(DictResult.NoCheck, abbreviation_glosbe.check_suspicion('tsk'))

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
            'printer',
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
            self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)

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
            self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion(word), word)

    def test_3word_notfound(self):
        words = [
            'col',
            'amb',
            'hup',
            ]
        for word in words:
            self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion(word), word)

    def test_3word_found(self):
        words = [
            'has',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)

    def test_found_else(self):
        words = [
            'gis',
            'pos',
            ]
        for word in words:
            self.assertNotEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)

    def test_past_found(self):
        words = [
            'ran',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)

    def test_plural_found(self):
        words = [
            'these',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)

    def test_plural_notfound(self):
        words = [
            'zos',
            ]
        for word in words:
            self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion(word), word)

    # gen'eration's
    def test_plural_abbreviation(self):
        words = [
            'certs',
            'gens',
            'subs',
            ]
        for word in words:
            self.assertEqual(DictResult.Abbreviation, abbreviation_glosbe.check_suspicion(word), word)

    def test_abbreviation_or_notfound(self):
        words = [
            'pos',
            ]
        for word in words:
            r = abbreviation_glosbe.check_suspicion(word)
            self.assertIn(r, [ DictResult.Abbreviation, DictResult.NotFound ], word)

    def test_misspelling(self):
        words = [
            'usefull',
            'extention',
            'repetetive',
            ]
        for word in words:
            self.assertEqual(DictResult.Misspelling, abbreviation_glosbe.check_suspicion(word), word)

    @unittest.skip("todo")
    def test_todo(self):
        words = [
            'resid',
            ]
        for word in words:
            self.assertEqual(DictResult.NotFound, abbreviation_glosbe.check_suspicion(word), word)

#    def test_2736(self):
#        words = [
#            'cannot',
#            'disallow',
#            'insensitive',
#            'mathematical',
#            'progress',
#            'resume',
#            'subject',
#            'useful',
#            ]
#        for word in words:
#            self.assertEqual(DictResult.Found, abbreviation_glosbe.check_suspicion(word), word)


if __name__ == '__main__':
    unittest.main()
