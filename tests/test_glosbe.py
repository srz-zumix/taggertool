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

    def test_found(self):
        words = [
            'pythagoras',
            'block',
            'posit',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)

    def test_abbreviation(self):
        words = [
            'vid',
            'abs',
            'chk',
            'min',
            'max',
            'neg',
            'semi',
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
            ]
        for word in words:
            self.assertEqual(DictResult.Misspelling, abbreviation.check_suspicion_glosbe(word), word)

    def test_no_support_dict_word(self):
        words = [
            ]
        for word in words:
            self.assertEqual(DictResult.NotFound, abbreviation.check_suspicion_glosbe(word), word)

    @unittest.skip('Response is unstable')
    def test_2736(self):
        words = [
            'mathematical',
            'useful',
            ]
        for word in words:
            self.assertEqual(DictResult.Found, abbreviation.check_suspicion_glosbe(word), word)


if __name__ == '__main__':
    unittest.main()
