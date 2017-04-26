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

    def test_tramp(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('tramp'))

    def test_topic(self):
        self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe('topic'))

    def test_found(self):
        words = [
#            'allocation',
#            'pot',
#            'repository',
            'role',
            'begin',
            'block',
            'compliment',
            'pat',
            'posit',
            'pythagoras',
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
