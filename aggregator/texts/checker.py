# coding: utf8

import logging

from nltk.stem.snowball import RussianStemmer, EnglishStemmer
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from collections import Counter
from math import log2
from re import sub
from json import loads

from config import constants
from ukr_stemmer import UkrainianStemmer

logger = logging.getLogger(constants.logger_name)


class CorrChecker(object):
    """ Text correctness checker class """

    def __init__(self, lang_info_path=constants.lang_info_path, stopwords_path=constants.stopwords_path):
        self.lang = None
        self.lang_info = self.load_json(lang_info_path)
        self.stopwords = self.load_json(stopwords_path)

    def __call__(self, string):
        """
        Check text correctness

        :param string: str
        :return: cleared text and language if correct else None
        """

        self.lang = self.detect_language(string)

        if self.lang is None:
            return -1

        try:
            self.lang_info[self.lang], self.stopwords[self.lang]

        except KeyError:
            return -2

        string, string_without_spaces = self.prepare(string)
        result = self.check_text_correctness(string_without_spaces)

        if result:
            string = self.stem_words(string.split())
            return self.delete_stop_words(string), self.lang

    @staticmethod
    def load_json(filename):
        """ Load language specific info from json """

        with open(filename, encoding=constants.load_encoding) as file:
            return loads(file.read())

    @staticmethod
    def detect_language(string):
        """ Detect string language by lang detect """

        try:
            return detect(string)

        except LangDetectException as e:
            logger.warning('Lang detect exception: {0}'.format(e))

    @staticmethod
    def bigram_frequency(string, step=1):
        f_dict = {}

        for i in range(0, len(string) - 1, step):
            if string[i] + string[i + 1] in f_dict:
                f_dict[string[i] + string[i + 1]] += 1
            else:
                f_dict[string[i] + string[i + 1]] = 1

        return f_dict

    @staticmethod
    def entropy(f_list, power, n=1):
        return -sum({i: f_list[i] / power * log2(f_list[i] / power) for i in f_list}.values()) / n

    def prepare(self, string):
        """ Clear input string according to the detected language """

        string = sub(r'[\n\t]| {2,}', ' ', string.lower())
        string = sub(r'[^{0}]'.format(self.lang_info[self.lang]['alphabet'] + ' '), '', string)
        string = sub(r' {2,}', ' ', string)
        string = sub(r'^ | $', '', string)

        if self.lang == 'uk':
            string = sub(r'[ґ]', 'г', string)

        elif self.lang == 'ru':
            string = sub(r'[ё]', 'е', string)

        return string, sub(r'[ ]', '', string)

    def stem_words(self, words):
        """ Stem words by Porter or Snowball stemmers and join to one string """

        stemmer = None

        if self.lang == 'uk':
            return ' '.join([UkrainianStemmer(word).stem_word() for word in words])

        elif self.lang == 'ru':
            stemmer = RussianStemmer()

        elif self.lang == 'en':
            stemmer = EnglishStemmer()

        return ' '.join([stemmer.stem(word) for word in words])

    def delete_stop_words(self, string):
        """ Delete stop words according to detected language """

        string = ' ' + string + ' '
        string = sub(r' ({0}) '.format('|'.join(self.stopwords[self.lang])), ' ', string)
        string = sub(r' {2,}', ' ', string)
        return sub(r'^ | $', '', string)

    def check_text_correctness(self, string):
        """ Check text correctness using h1 and h2 entropic criteria """

        h1_cr = self.entropy(Counter(string), len(string)) < self.lang_info[self.lang]['h1']
        h2_cr = self.entropy(self.bigram_frequency(string), len(string), n=2) < self.lang_info[self.lang]['h2']
        return h1_cr and h2_cr


if __name__ == '__main__':
    checker = CorrChecker()
    check_result = checker('Міжнародний фестиваль "Книжковий Арсенал" стартує у столиці.')
    print('Cleared text: {0}, language: {1}'.format(*check_result))
