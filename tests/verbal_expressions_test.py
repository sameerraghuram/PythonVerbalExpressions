# -*- encoding: utf-8 -*-
import unittest
from verbalexpressions import VerEx
import re
import sys

class VerExTest(unittest.TestCase):
    '''
        Tests for verbal_expressions.py
    '''
        
    def setUp(self):
        self.v = VerEx()
        if sys.version_info[0] < 3:
            self.assertRegex = self.assertRegexpMatches
            self.assertNotRegex = self.assertNotRegexpMatches

    def tearDown(self):
        self.v = None
        self.exp = None

    def test_should_render_verex_as_string(self):
        self.assertEqual(str(self.v.add('^$')), '^$')

    def test_should_render_verex_list_as_string(self):
        self.assertEqual(str(self.v.add(['^', '[0-9]', '$'])), '^[0-9]$')

    def test_should_match_characters_in_range(self):
        self.exp = self.v.start_of_line().range('a', 'c').regex()
        for character in ['a', 'b', 'c']:
            self.assertRegex(character, self.exp)

    def test_should_not_match_characters_outside_of_range(self):
        self.exp = self.v.start_of_line().range('a', 'c').regex()
        self.assertNotRegex('d', self.exp)

    def test_should_match_characters_in_extended_range(self):
        self.exp = self.v.start_of_line().range('a', 'b', 'X', 'Z').regex()
        for character in ['a', 'b']:
            self.assertRegex(character, self.exp)
        for character in ['X', 'Y', 'Z']:
            self.assertRegex(character, self.exp)

    def test_should_not_match_characters_outside_of_extended_range(self):
        self.exp = self.v.start_of_line().range('a', 'b', 'X', 'Z').regex()
        self.assertNotRegex('c', self.exp)
        self.assertNotRegex('W', self.exp)


    def test_should_match_start_of_line(self):
        self.exp = self.v.start_of_line().regex()
        self.assertRegex('text  ', self.exp, 'Not started :(')

    def test_should_match_end_of_line(self):
        self.exp = self.v.start_of_line().end_of_line().regex()
        self.assertRegex('', self.exp, 'It\'s not the end!')

    def test_should_match_anything(self):
        self.exp = self.v.start_of_line().anything().end_of_line().regex()
        self.assertRegex('!@#$%¨&*()__+{}', self.exp, 'Not so anything...')

    def test_should_match_anything_but_specified_element_when_element_is_not_found(self):
        self.exp = self.v.start_of_line().anything_but('X').end_of_line().regex()
        self.assertRegex('Y Files', self.exp, 'Found the X!')

    def test_should_not_match_anything_but_specified_element_when_specified_element_is_found(self):
        self.exp = self.v.start_of_line().anything_but('X').end_of_line().regex()
        self.assertNotRegex('VerEX', self.exp, 'Didn\'t found the X :(')

    def test_should_find_element(self):
        self.exp = self.v.start_of_line().find('Wally').end_of_line().regex()
        self.assertRegex('Wally', self.exp, '404! Wally not Found!')

    def test_should_not_find_missing_element(self):
        self.exp = self.v.start_of_line().find('Wally').end_of_line().regex()
        self.assertNotRegex('Wall-e', self.exp, 'DAFUQ is Wall-e?')

    def test_should_match_when_maybe_element_is_present(self):
        self.exp = self.v.start_of_line().find('Python2.').maybe('7').end_of_line().regex()
        self.assertRegex('Python2.7', self.exp, 'Version doesn\'t match!')

    def test_should_match_when_maybe_element_is_missing(self):
        self.exp = self.v.start_of_line().find('Python2.').maybe('7').end_of_line().regex()
        self.assertRegex('Python2.', self.exp, 'Version doesn\'t match!')

    def test_should_match_on_any_when_element_is_found(self):
        self.exp = self.v.start_of_line().any('Q').anything().end_of_line().regex()
        self.assertRegex('Query', self.exp, 'No match found!')

    def test_should_not_match_on_any_when_element_is_not_found(self):
        self.exp = self.v.start_of_line().any('Q').anything().end_of_line().regex()
        self.assertNotRegex('W', self.exp, 'I\'ve found it!')

    def test_should_match_when_line_break_present(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertRegex('Marco \n Polo', self.exp, 'Give me a break!!')

    def test_should_match_when_line_break_and_carriage_return_present(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertRegex('Marco \r\n Polo', self.exp, 'Give me a break!!')

    def test_should_not_match_when_line_break_is_missing(self):
        self.exp = self.v.start_of_line().anything().line_break().anything().end_of_line().regex()
        self.assertNotRegex('Marco Polo', self.exp, 'There\'s a break here!')

    def test_should_match_when_tab_present(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertRegex('One tab only	', self.exp, 'No tab here!')

    def test_should_not_match_when_tab_is_missing(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'No tab here'), 'There\'s a tab here!')

    def test_should_match_when_word_present(self):
        self.exp = self.v.start_of_line().anything().word().end_of_line().regex()
        self.assertRegex('Oneword', self.exp, 'Not just a word!')

    def test_not_match_when_two_words_are_present_instead_of_one(self):
        self.exp = self.v.start_of_line().anything().tab().end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Two words'), 'I\'ve found two of them')

    def test_should_match_when_or_condition_fulfilled(self):
        self.exp = self.v.start_of_line().anything().find('G').OR().find('h').end_of_line().regex()
        self.assertRegex('Github', self.exp, 'Octocat not found')

    def test_should_not_match_when_or_condition_not_fulfilled(self):
        self.exp = self.v.start_of_line().anything().find('G').OR().find('h').end_of_line().regex()
        self.assertFalse(re.match(self.exp, 'Bitbucket'), 'Bucket not found')

    def test_should_match_on_upper_case_when_lower_case_is_given_and_any_case_is_true(self):
        self.exp = self.v.start_of_line().find('THOR').end_of_line().with_any_case(True).regex()
        self.assertRegex('thor', self.exp, 'Upper case Thor, please!')

    def test_should_match_multiple_lines(self):
        self.exp = self.v.start_of_line().anything().find('Pong').anything().end_of_line().search_one_line(True).regex()
        self.assertRegex('Ping \n Pong \n Ping', self.exp, 'Pong didn\'t answer')

    def test_should_match_email_address(self):
        self.exp = self.v.start_of_line().word().then('@').word().then('.').word().end_of_line().regex()
        self.assertRegex('mail@mail.com', self.exp, 'Not a valid email')

    def test_should_match_url(self):
        self.exp = self.v.start_of_line().then('http').maybe('s').then('://').maybe('www.').word().then('.').word().maybe('/').end_of_line().regex()
        self.assertRegex('https://www.google.com/', self.exp, 'Not a valid email')
