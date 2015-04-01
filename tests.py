#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import staircase as t

DICTIONARY = t.read_dictionary("runouns.txt")


class Test(unittest.TestCase):

    def assertIsChain(self, chain, start, end):
        self.assertIsNotNone(chain)
        self.assertEqual(chain[0], start)
        self.assertEqual(chain[-1], end)

    def test_incorrect_chain(self):
        dictionary = DICTIONARY[4]
        self.assertIsNone(t.find_chain("ываа", "фывф", dictionary))

    def test_correct_chain(self):
        start = "мама"
        end = "папа"
        dictionary = DICTIONARY[4]
        result = t.find_chain(start, end, dictionary)
        self.assertIsChain(result, start, end)

    def test_long_chain(self):
        start = "школа"
        end = "танец"
        dictionary = DICTIONARY[5]
        result = t.find_chain(start, end, dictionary)
        self.assertIsChain(result, start, end)

    def test_one_word(self):
        start = end = "а"
        dictionary = DICTIONARY[1]
        result = t.find_chain(start, end, dictionary)
        self.assertIsChain(result, start, end)

    def test_diff_length(self):
        dictionary = DICTIONARY[4]
        self.assertIsNone(t.find_chain("корова", "бык", dictionary))

if __name__ == '__main__':
    unittest.main()
