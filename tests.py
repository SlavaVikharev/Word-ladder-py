#!/usr/bin/env python3

import unittest
from ladder import StaircaseTools as STools

DICTIONARY = STools.read_dictionary("runouns.txt")


class Test(unittest.TestCase):

    def assert_is_chain(self, chain, start, end):
        self.assertNotEqual(len(chain), 0)
        self.assertEqual(chain[0], start)
        self.assertEqual(chain[-1], end)

    def test_read_dictionary(self):
        dictionary = STools.read_dictionary("testdict.txt")
        self.assertEqual(len(dictionary), 2)
        self.assertEqual(len(dictionary[4]), 7)
        self.assertEqual(len(dictionary[3]), 1)
        for word in dictionary[3]:
            self.assertEqual(word, word.lower())
        dictionary = STools.read_dictionary("testdict.txt", False)
        self.assertEqual(len(dictionary), 2)
        self.assertEqual(len(dictionary[4]), 7)
        self.assertEqual(len(dictionary[3]), 2)

    def test_correct_input(self):
        correct_input = STools.correct_input("муха", "слон", DICTIONARY[4])
        self.assertTrue(correct_input)
        correct_input = STools.correct_input("ыва", "ываы", DICTIONARY[4])
        self.assertFalse(correct_input)

    def test_incorrect_chain(self):
        chains = STools.find_shortest_chain("ываа", "фывф", DICTIONARY[4])
        self.assertEqual(len(chains), 0)

    def test_is_similar(self):
        self.assertFalse(STools.is_similar("торт", "шар"))
        self.assertFalse(STools.is_similar("торт", "торт"))
        self.assertTrue(STools.is_similar("кот", "код"))

    def test_correct_chain(self):
        start = "мама"
        end = "папа"
        dictionary = DICTIONARY[4]
        chain = STools.find_shortest_chain(start, end, dictionary)
        self.assert_is_chain(chain, start, end)

    def test_long_chain(self):
        start = "школа"
        end = "танец"
        dictionary = DICTIONARY[5]
        chain = STools.find_shortest_chain(start, end, dictionary)
        self.assert_is_chain(chain, start, end)

    def test_one_word_all_chains(self):
        start = end = "а"
        dictionary = DICTIONARY[1]
        chains = STools.find_all_chains(start, end, dictionary, 3)
        self.assertEqual(len(chains), 1)
        for chain in chains:
            self.assert_is_chain(chain, start, end)

    def test_all_chains(self):
        start = "1111"
        end = "2101"
        dictionary = STools.read_dictionary("testdict.txt")[4]
        chains = STools.find_all_chains(start, end, dictionary, 5)
        self.assertEqual(len(chains), 4)
        for chain in chains:
            self.assert_is_chain(chain, start, end)

    def test_diff_length(self):
        dictionary = DICTIONARY[4]
        chains = STools.find_shortest_chain("корова", "бык", dictionary)
        self.assertEqual(len(chains), 0)

if __name__ == '__main__':
    unittest.main()
