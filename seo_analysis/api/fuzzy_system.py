import pickle
import logging
from numpy import arange
from skfuzzy import control, trimf
from collections import Counter
from math import sqrt
from config import constants

logger = logging.getLogger(constants.logger_name)


class SEOAnalyzer(object):
    """ Class that provides computing main metrics for SEO analysis """

    classic_min_value = 2.64

    def __call__(self, string):
        frequencies = Counter(string.split())
        return self.nausea_classic(frequencies), self.nausea_academic(frequencies)

    def nausea_classic(self, frequencies):
        """ Compute text`s classic nausea """

        result = sqrt(frequencies.most_common(1)[0][1])

        if result < self.classic_min_value:
            return self.classic_min_value

        return result

    @staticmethod
    def nausea_academic(frequencies):
        """ Compute text`s academic nausea """

        return (frequencies.most_common(1)[0][1] / sum(frequencies.values())) * 100


class FuzzyControlSystem(object):
    """ Fuzzy control system for evaluating text SEO processing """

    def __init__(self, filename=constants.fuzzy_system_path):
        self.system = None
        self.filename = filename
        self.analyzer = SEOAnalyzer()

        # load created system if exists

        try:
            self.load_model(self.filename)

        except IOError:
            self.create()
            self.save_model()

    def __str__(self):
        return 'Fuzzy control system. ' + 'System: created.' if self.system is not None else 'System: None.'

    def check_system(self):
        if self.system is None:
            raise ValueError('Create fuzzy system first')

    def create(self, step=0.1, interval=(0, 1.1)):
        """
        Create fuzzy control system

        :param step: interval step
        :param interval: interval of output fuzzy variable values
        """

        # input variables

        ns_classic = control.Antecedent(arange(2.6, 50, step), 'ns_classic')
        ns_academic = control.Antecedent(arange(1, 100, step), 'ns_academic')

        # output variables

        mark = control.Consequent(arange(*interval, step), 'mark')

        # membership functions for input and output fuzzy variables

        ns_classic['poor'] = trimf(ns_classic.universe, (7, 7, 50))
        ns_classic['average'] = trimf(ns_classic.universe, (4, 5.5, 7))

        ns_classic['good'] = trimf(ns_classic.universe,
                                   (SEOAnalyzer.classic_min_value, SEOAnalyzer.classic_min_value, 4))

        ns_academic['poor'] = trimf(ns_academic.universe, (20, 20, 100))
        ns_academic['average'] = trimf(ns_academic.universe, (10, 15, 20))
        ns_academic['good'] = trimf(ns_academic.universe, (1, 1, 10))

        mark.automf(3)

        # rules

        r1 = control.Rule(ns_classic['poor'] | ns_academic['poor'], mark['poor'] % 1.0)
        r2 = control.Rule(ns_classic['average'] & ns_academic['average'], mark['average'] % 0.8)
        r3 = control.Rule(ns_classic['good'] & ns_academic['average'], mark['average'] % 0.8)
        r4 = control.Rule(ns_classic['average'] & ns_academic['good'], mark['average'] % 0.8)
        r5 = control.Rule(ns_classic['good'] & ns_academic['good'], mark['good'] % 1.0)

        self.system = control.ControlSystemSimulation(control.ControlSystem([r1, r2, r3, r4, r5]))

    def evaluate(self, string):
        """ Compute control system output by given input string """

        self.check_system()

        inputs = self.analyzer(string)
        self.system.input['ns_classic'], self.system.input['ns_academic'] = inputs

        try:
            self.system.compute()

        except ValueError:
            logger.warning('Defuzzification failed for inputs: {0}'.format(inputs))
            return

        return self.system.output['mark']

    def print_state(self):
        """ Print info about fuzzy system, evaluate method should be called first """

        self.check_system()

        try:
            self.system.print_state()

        except ValueError:
            print('Call evaluate method first.')

    def load_model(self, filename):
        """ Load previously created fuzzy system from binary file """

        with open(filename, 'rb') as file:
            self.system = pickle.load(file)

    def save_model(self):
        """ Save created fuzzy system by pickle """

        self.check_system()

        with open(self.filename, 'wb') as file:
            pickle.dump(self.system, file)


control_system = FuzzyControlSystem()
