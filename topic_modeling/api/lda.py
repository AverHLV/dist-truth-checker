# coding: utf8

import csv
import pickle
import pandas as pd

from numpy import argmax, array
from pyLDAvis import show
from pyLDAvis.sklearn import prepare
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from scipy.spatial.distance import jensenshannon
from nltk.stem.snowball import RussianStemmer, EnglishStemmer

from collections import Counter
from re import sub
from json import loads

from config import constants
from ukr_stemmer import UkrainianStemmer


class Corpora(object):
    """ Managing text collections class for use in LDA algorithm """

    def __init__(self,
                 clear=False,
                 filename='corpora/ru.csv',
                 filename_for_save=None,
                 min_string_length=100,
                 tf_idf_thresholds=(2, 7),
                 stopwords_filename='json/stopwords.json',
                 alphabets_filename='json/alphabets.json'):
        """
        Corpora class initialization

        :param clear: clear loaded corpora or not
        :param filename: csv filename for load, should be in format *??.csv, where ?? - language code
        :param filename_for_save: filename with csv format for saving corpora
        :param min_string_length: minimum possible string length in corpora
        :param tf_idf_thresholds: pair of lower and upper thresholds for clearing by tf-idf value
        :param stopwords_filename: stopwords filename in json format
        :param alphabets_filename: language alphabets in json format
        """

        self.filename_for_save = filename_for_save
        self.lang = filename[filename.rfind('.') - 2:filename.rfind('.')]

        # load data

        self.stopwords = self.load_json(stopwords_filename)[self.lang]
        self.alphabet = self.load_json(alphabets_filename)[self.lang]
        self.__corpora = self.load_corpora(filename)
        self.join_strings()

        if clear:
            # clear corpora

            self.prepare()
            self.delete_small_strings(min_string_length)
            self.stem_text()
            self.delete_words()
            self.tf_idf(tf_idf_thresholds)
            self.clean_spaces()
            self.delete_small_strings(min_string_length)

            # save results

            self.save_corpora()

    @property
    def corpora(self):
        return self.__corpora

    @staticmethod
    def load_corpora(filename):
        """ Load specified corpora in csv format """

        with open(filename, encoding=constants.load_encoding) as file:
            return list(csv.reader(file))

    @staticmethod
    def load_json(filename):
        """ Load specific info in json format """

        with open(filename, encoding=constants.load_encoding) as file:
            return loads(file.read())

    def join_strings(self):
        """ Join all lists in row to one string """

        self.__corpora = [' ' + ' '.join(strings) + ' ' for strings in self.__corpora]

    def prepare(self):
        """ Clear corpora according to the specified language """

        for i in range(len(self.__corpora)):
            string = self.__corpora[i]
            string = sub(r'[\n\t]| {2,}', ' ', string.lower())
            string = sub(r'[^{0}]'.format(self.alphabet + ' '), '', string)

            if self.lang == 'uk':
                string = sub(r'[ґ]', 'г', string)

            elif self.lang == 'ru':
                string = sub(r'[ё]', 'е', string)

            self.__corpora[i] = string

    def clean_spaces(self):
        for i in range(len(self.__corpora)):
            if len(self.__corpora[i]):
                self.__corpora[i] = sub(r' {2,}', ' ', self.__corpora[i])
                self.__corpora[i] = sub(r'^ | $', '', self.__corpora[i])

    def stem_text(self):
        """ Stem words by Porter or Snowball stemmers """

        stemmer = None

        if self.lang == 'ru':
            stemmer = RussianStemmer()

        elif self.lang == 'en':
            stemmer = EnglishStemmer()

        for i in range(len(self.__corpora)):
            words = self.__corpora[i].split()

            if self.lang == 'uk':
                self.__corpora[i] = ' '.join([UkrainianStemmer(word).stem_word() for word in words])

            else:
                self.__corpora[i] = ' '.join([stemmer.stem(word) for word in words])

    def delete_words(self, words=None):
        """ Delete specific words or stopwords from corpora """

        if words is None:
            words = self.stopwords

        self.__corpora = [
            sub(r' ({0}) '.format('|'.join(words)), ' ', string) for string in self.__corpora
        ]

    def tf_idf(self, thresholds):
        """ Delete uninformative words by TF-IDF value """

        if thresholds[0] >= thresholds[1]:
            raise ValueError('Thresholds[0] must be lower than thresholds[1]')

        vectorizer = TfidfVectorizer(lowercase=False)
        vectorizer.fit(self.__corpora)

        features = vectorizer.get_feature_names()
        values = vectorizer.idf_
        words = [features[i] for i in range(len(values)) if values[i] < thresholds[0] or values[i] > thresholds[1]]

        if len(words):
            self.delete_words(words)

    def delete_small_strings(self, min_string_length):
        """ Delete very small strings from corpora """

        self.__corpora = [string for string in self.__corpora if len(string) >= min_string_length]

    def most_common(self, number=10):
        """ Display %number% most common words in corpora """

        words_full_list = []

        for string in self.__corpora:
            words_full_list += string.split()

        print(Counter(words_full_list).most_common(number))

    def save_corpora(self):
        """ Save corpora to csv """

        if self.filename_for_save is not None:
            with open(self.filename_for_save, 'w', newline='', encoding=constants.load_encoding) as file:
                writer = csv.writer(file)

                for string in self.__corpora:
                    writer.writerow([string])


class LDA(object):
    """ Class for Latent Dirichlet Allocation model """

    def __init__(self, filename):
        self.filename = filename
        self.vectorized_data = None
        self.df_topic_keywords = None
        self.fitted = False

        # load fitted model if exists

        try:
            self.load_model(self.filename)
            self.fitted = True

        except IOError:
            self.vectorizer = CountVectorizer(lowercase=False)
            self.model = LatentDirichletAllocation()

    def __str__(self):
        print_string = 'LDA model. Params:\n'
        params = self.model.get_params()

        for key in params:
            print_string += '{0}: {1}\n'.format(key, params[key])

        return print_string

    def check_model(self):
        if not self.fitted or self.model is None:
            raise ValueError('Model is not fitted or not created')

    def fit(self, corpora):
        """
        Fit LDA model by texts collection

        :param corpora: list of str
        """

        self.vectorized_data = self.vectorizer.fit_transform(corpora)

        search_params = {'n_components': [10, 15, 20, 25, 30]}
        model = GridSearchCV(self.model, param_grid=search_params, cv=3)
        model.fit(self.vectorized_data)

        self.model = model.best_estimator_
        self.fitted = True
        self.construct_df_topics()
        self.save_model()

    def predict(self, text, distribution_only=True):
        """
        Predict most relevant words for given text

        :param text: str
        :param distribution_only: bool, compute only document-topics distribution
        :return: list of (keyword, probability score)
        """

        self.check_model()

        if distribution_only:
            return self.model.transform(self.vectorizer.transform(text))

        topic_probability_scores = self.model.transform(self.vectorizer.transform(text))[0]
        topics = self.df_topic_keywords.iloc[argmax(topic_probability_scores), :].values.tolist()
        topics = list(zip(topics, topic_probability_scores))
        return sorted(topics, key=lambda x: x[1], reverse=True)

    def compute_similarity(self, text1, text2):
        """
        Compute the Jensen-Shannon distance between probability arrays of two texts

        :param text1: list of str
        :param text2: list of str
        :return: float in [0, 1], bigger - less similar
        """

        text1_dist = self.predict(text1)[0]
        text2_dist = self.predict(text2)[0]
        return jensenshannon(text1_dist, text2_dist)

    def construct_df_topics(self, n_words=20):
        """ Construct pd.DataFrame with top %n_words% keywords for each topic """

        self.check_model()
        topic_keywords = []
        keywords = array(self.vectorizer.get_feature_names())

        for topic_weights in self.model.components_:
            top_keyword_locs = (-topic_weights).argsort()[:n_words]
            topic_keywords.append(keywords.take(top_keyword_locs))

        self.df_topic_keywords = pd.DataFrame(topic_keywords)
        self.df_topic_keywords.columns = ['Word ' + str(i) for i in range(self.df_topic_keywords.shape[1])]
        self.df_topic_keywords.index = ['Topic ' + str(i) for i in range(self.df_topic_keywords.shape[0])]

    def stats(self):
        self.check_model()
        print('Log Likelihood:', self.model.score(self.vectorized_data))
        print('Perplexity:', self.model.perplexity(self.vectorized_data))

    def visualize(self):
        """ Start local web-server and display LDA fitted model """

        self.check_model()
        show(prepare(self.model, self.vectorized_data, self.vectorizer, mds='tsne'))

    def load_model(self, filename):
        """ Load LDA model, CountVectorizer instance and term-document matrix from binary file """

        with open(filename, 'rb') as file:
            model_dict = pickle.load(file)

        self.model = model_dict['model']
        self.vectorizer = model_dict['vec']
        self.vectorized_data = model_dict['vec_data']
        self.df_topic_keywords = model_dict['df']

    def save_model(self):
        """ Save fitted LDA model by pickle """

        self.check_model()

        with open(self.filename, 'wb') as file:
            pickle.dump({'model': self.model, 'vec': self.vectorizer, 'vec_data': self.vectorized_data,
                         'df': self.df_topic_keywords}, file)


if __name__ == '__main__':
    # texts with different topics

    one_text = ['ціну газу для промспоживачів знизять коли і на скільки']
    another_text = ['суд в криму залишив під арештом сервера мустафава']

    lda_uk = LDA(filename='models/lda_uk.model')
    print(lda_uk.compute_similarity(one_text, another_text))
