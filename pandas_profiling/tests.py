# coding=UTF-8

import unittest

import datetime
import numpy as np
import pandas as pd
import six
import pandas_profiling
from pandas_profiling.base import describe, to_html
import tempfile
import shutil
import os
check_is_NaN = "pandas_profiling.check_is_NaN"


class DataFrameTest(unittest.TestCase):

    def setUp(self):
        self.data = {'id': [chr(97+c) for c in range(1,10)],
                     'x': [50, 50, -10, 0, 0, 5, 15, -3, None],
                     'y': [0.000001, 654.152, None, 15.984512, 3122, -3.1415926535, 111, 15.9, 13.5],
                     'cat': ['a', 'long text value', u'Élysée', '', None, 'some <b> B.s </div> </div> HTML stuff', 'c',
                             'c',
                             'c'],
                     's1': np.ones(9),
                     's2': [u'some constant text $ % value {obj} ' for _ in range(1, 10)],
                     'somedate': [datetime.date(2011, 7, 4), datetime.datetime(2022, 1, 1, 13, 57),
                                  datetime.datetime(1990, 12, 9), np.nan,
                                  datetime.datetime(1990, 12, 9), datetime.datetime(1950, 12, 9),
                                  datetime.datetime(1898, 1, 2), datetime.datetime(1950, 12, 9)
                         , datetime.datetime(1950, 12, 9)]}
        self.df = pd.DataFrame(self.data)
        self.df['somedate'] = pd.to_datetime(self.df['somedate'])

        self.results = describe(self.df)
        self.test_dir = tempfile.mkdtemp()


    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_describe_df(self):

        expected_results = {}
        expected_results['id'] = {'25%': check_is_NaN, '5%': check_is_NaN, '50%': check_is_NaN, '75%': check_is_NaN, '95%': check_is_NaN, 'count': 9, 'n_infinite': 0, 'p_infinite': 0,
                                  'cv': check_is_NaN, 'distinct_count': 9, 'freq': check_is_NaN, 'histogram': check_is_NaN, 'iqr': check_is_NaN,
                                  'is_unique': True, 'kurtosis': check_is_NaN, 'mad': check_is_NaN, 'max': check_is_NaN, 'mean': check_is_NaN,
                                  'min': check_is_NaN, 'mini_histogram': check_is_NaN, 'n_missing': 0, 'p_missing': 0.0,
                                  'p_unique': 1.0, 'p_zeros': check_is_NaN, 'range': check_is_NaN, 'skewness': check_is_NaN,
                                  'std': check_is_NaN, 'sum': check_is_NaN, 'top': check_is_NaN, 'type': 'UNIQUE', 'variance': check_is_NaN}
        expected_results['x'] = {'25%': -0.75, '5%': -7.5499999999999989, '50%': 2.5, '75%': 23.75, '95%': 50.0,
                                 'count': 8, 'n_infinite': 0, 'p_infinite': 0, 'cv': 1.771071190261633, 'distinct_count': 7, 'freq': check_is_NaN, 'iqr': 24.5,
                                 'is_unique': False, 'kurtosis': -0.50292858929003803, 'mad': 18.71875, 'max': 50.0,
                                 'mean': 13.375, 'min': -10.0, 'mode': 0.0, 'n_missing': 1,
                                 'p_missing': 0.11111111111111116, 'p_unique': 0.875, 'p_zeros': 0.2222222222222222,
                                 'range': 60.0, 'skewness': 1.0851622393567653, 'std': 23.688077169749342, 'sum': 107.0,
                                 'top': check_is_NaN, 'type': 'NUM', 'variance': 561.125}
        expected_results['y'] = {'25%': 10.125000249999999, '5%': -2.0420348747749997, '50%': 15.942256,
                                 '75%': 246.78800000000001, '95%': 2258.2531999999987, 'count': 8, 'n_infinite': 0, 'p_infinite': 0,
                                 'cv': 2.2112992878833846, 'distinct_count': 9, 'freq': check_is_NaN,
                                 'iqr': 236.66299975000001, 'is_unique': True, 'kurtosis': 6.974137018717359,
                                 'mad': 698.45081747834365, 'max': 3122.0, 'mean': 491.17436504331249,
                                 'min': -3.1415926535000001, 'mode': 9.9999999999999995e-07, 'n_missing': 1,
                                 'p_missing': 0.11111111111111116, 'p_unique': 1.125, 'p_zeros': 0.0,
                                 'range': 3125.1415926535001, 'skewness': 2.6156591135729266, 'std': 1086.1335236468506,
                                 'sum': 3929.3949203464999, 'top': check_is_NaN, 'type': 'NUM',
                                 'variance': 1179686.0311895239}
        expected_results['cat'] = {'25%': check_is_NaN, '5%': check_is_NaN, '50%': check_is_NaN, '75%': check_is_NaN, '95%': check_is_NaN, 'count': 8, 'n_infinite': 0, 'p_infinite': 0,
                                   'cv': check_is_NaN, 'distinct_count': 7, 'freq': 3, 'histogram': check_is_NaN, 'iqr': check_is_NaN,
                                   'is_unique': False, 'kurtosis': check_is_NaN, 'mad': check_is_NaN, 'max': check_is_NaN, 'mean': check_is_NaN,
                                   'min': check_is_NaN, 'mini_histogram': check_is_NaN, 'mode': 'c',
                                   'n_missing': 1, 'p_missing': 0.11111111111111116, 'p_unique': 0.875,
                                   'p_zeros': check_is_NaN, 'range': check_is_NaN, 'skewness': check_is_NaN, 'std': check_is_NaN, 'sum': check_is_NaN,
                                   'top': 'c', 'type': 'CAT', 'variance': check_is_NaN}
        expected_results['s1'] = {'25%': check_is_NaN, '5%': check_is_NaN, '50%': check_is_NaN, '75%': check_is_NaN, '95%': check_is_NaN, 'count': 9, 'n_infinite': 0, 'p_infinite': 0,
                                  'cv': check_is_NaN, 'distinct_count': 1, 'freq': check_is_NaN, 'histogram': check_is_NaN, 'iqr': check_is_NaN,
                                  'is_unique': False, 'kurtosis': check_is_NaN, 'mad': check_is_NaN, 'max': check_is_NaN, 'mean': check_is_NaN,
                                  'min': check_is_NaN, 'mini_histogram': check_is_NaN, 'mode': 1.0,
                                  'n_missing': 0, 'p_missing': 0.0, 'p_unique': 0.1111111111111111, 'p_zeros': check_is_NaN,
                                  'range': check_is_NaN, 'skewness': check_is_NaN, 'std': check_is_NaN, 'sum': check_is_NaN, 'top': check_is_NaN,
                                  'type': 'CONST', 'variance': check_is_NaN}
        expected_results['s2'] = {'25%': check_is_NaN, '5%': check_is_NaN, '50%': check_is_NaN, '75%': check_is_NaN, '95%': check_is_NaN, 'count': 9, 'n_infinite': 0, 'p_infinite': 0,
                                  'cv': check_is_NaN, 'distinct_count': 1, 'freq': check_is_NaN, 'histogram': check_is_NaN, 'iqr': check_is_NaN,
                                  'is_unique': False, 'kurtosis': check_is_NaN, 'mad': check_is_NaN, 'max': check_is_NaN, 'mean': check_is_NaN,
                                  'min': check_is_NaN, 'mini_histogram': check_is_NaN,
                                  'mode': u'some constant text $ % value {obj} ', 'n_missing': 0, 'p_missing': 0.0,
                                  'p_unique': 0.1111111111111111, 'p_zeros': check_is_NaN, 'range': check_is_NaN,
                                  'skewness': check_is_NaN, 'std': check_is_NaN, 'sum': check_is_NaN, 'top': check_is_NaN, 'type': 'CONST',
                                  'variance': check_is_NaN}
        expected_results['somedate'] = {'25%': check_is_NaN, '5%': check_is_NaN, '50%': check_is_NaN, '75%': check_is_NaN, '95%': check_is_NaN,
                                        'count': 8, 'n_infinite': 0, 'p_infinite': 0, 'cv': check_is_NaN, 'distinct_count': 6, 'freq': check_is_NaN,
                                        'iqr': check_is_NaN, 'is_unique': False, 'kurtosis': check_is_NaN,
                                        'mad': check_is_NaN, 'max': datetime.datetime(2022, 1, 1, 13, 57), 'mean': check_is_NaN,
                                        'min': datetime.datetime(1898, 1, 2),
                                        'mode': datetime.datetime(1950, 12, 9),
                                        'n_missing': 1, 'p_missing': 0.11111111111111116, 'p_unique': 0.75,
                                        'p_zeros': check_is_NaN, 'range': datetime.timedelta(45289, hours=13, minutes=57),
                                        'skewness': check_is_NaN, 'std': check_is_NaN, 'sum': check_is_NaN, 'top': check_is_NaN, 'type': 'DATE',
                                        }

        self.assertSetEqual(set(self.results.keys()), set(['table', 'variables', 'freq']))
        self.assertSetEqual(set(self.results['freq'].keys()), set(self.data.keys()))
        self.assertSetEqual(set(self.results['variables'].index), set(self.data.keys()))

        self.assertTrue(set({'CAT': 1,
                                       'CONST': 2,
                                       'DATE': 1,
                                       'NUM': 2,
                                       'UNIQUE': 1,
                                       'n': 9,
                                       'n_duplicates': 0,
                                       'nvar': 7,
                                       }.items()).issubset(set(self.results['table'].items())))

        self.assertAlmostEqual(0.063492063492063489, self.results['table']['total_missing'], 7)
        # Loop over variables
        for col in self.data.keys():
            for k,v in six.iteritems(expected_results[col]):
                if v == check_is_NaN:
                    self.assertTrue(np.isnan(self.results['variables'].loc[col][k]), msg="Value {} for key {} in column {} is not NaN".format(self.results['variables'].loc[col][k], k, col))
                elif isinstance(v, float):
                    self.assertAlmostEqual(v, self.results['variables'].loc[col][k], 7)
                else:
                    self.assertEqual(v, self.results['variables'].loc[col][k])

            if self.results['variables'].loc[col]['type'] in ['NUM', 'DATE']:
                self.assertLess(200, len(self.results['variables'].loc[col]["histogram"]),
                                "Histogram missing for column %s " % col)
                self.assertLess(200, len(self.results['variables'].loc[col]["mini_histogram"]),
                                "Mini-histogram missing for column %s " % col)


    def test_html_report(self):
        html = to_html(self.df.head(), self.results)
        self.assertLess(1000, len(html))

    def test_bins(self):
        self.results = describe(self.df, bins=100)
        self.test_describe_df()

    def test_export_to_file(self):

        p = pandas_profiling.ProfileReport(self.df)
        filename = os.path.join(self.test_dir, "profile_%s.html" % hash(self))
        p.to_file(outputfile=filename)

        self.assertLess(200,os.path.getsize(filename))


class CategoricalDataTest(unittest.TestCase):

    def test_recoding_reject(self):
        self.data = {
             'x': ['chien', 'chien', 'chien', 'chien', 'chat','chat','chameaux', 'chameaux'],
             'y': ['dog', 'dog', 'dog', 'dog', 'cat','cat','camel','camel'],
           }
        self.df = pd.DataFrame(self.data)
        self.results = describe(self.df)

        self.assertEqual(self.results['variables'].loc['x']['type'], 'RECODED')
        self.assertEqual(self.results['variables'].loc['x']['correlation_var'], 'y')

        expected_results = {'total_missing': 0.0, 'UNIQUE': 0, 'CONST': 0, 'nvar': 2, 'REJECTED': 1, 'n': 8, 'RECODED': 1, 'CORR': 0, 'DATE': 0, 'NUM': 0, 'CAT': 1, 'n_duplicates': 5}
        for key in expected_results:
            self.assertEqual(self.results['table'][key], expected_results[key])


if __name__ == '__main__':
    unittest.main()
