# %%
import os

os.chdir("C:\Dropbox\Desenvolvimento\Proprio\studies\study-datascience\pandas-profiling\pandas_profiling")

# %%
if __name__ == '__main__':
    import pandas_profiling
    import pandas as pd
    import numpy as np

    # import re
    # regex = r"(?P<alpha>[a-zA-Z])|(?P<blank>\s)|(?P<digit>\d)|(?P<non_word>\W)"
    #
    # test_str = "teste asdassadasd12312dasds   asdasd 121233 adasds@@dasd123123  dsada$%$^^\\n"
    #
    # matches = re.finditer(regex, test_str)
    #
    # for matchNum, match in enumerate(matches):
    #     matchNum = matchNum + 1
    #
    #     print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
    #                                                                         end=match.end(), match=match.group()))
    #
    #     for groupNum in range(0, len(match.groups())):
    #         groupNum = groupNum + 1
    #
    #         print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
    #                                                                         start=match.start(groupNum),
    #                                                                         end=match.end(groupNum),
    #                                                                         group=match.group(groupNum)))

    # df = pd.read_csv("../examples/villes_france.csv", encoding='UTF-8')
    # pfr = pandas_profiling.ProfileReport(df, check_recoded=False)
    # pfr.to_file("/tmp/example.html")

    # df = pd.read_csv("../examples/villes_france.csv", dtype={'dep': str, 'code insee': str}, encoding='UTF-8')
    # pfr = pandas_profiling.ProfileReport(df, check_correlation=False)
    # pfr.to_file("/tmp/example.html")

    # df = pd.DataFrame(dict(a=[1, "A", np.nan], b=[[1, 2], [3, 4], np.nan], c=[1, 2, 3]))
    #
    # # data = df['a']
    # #
    # # value_counts_with_nan = data.value_counts(dropna=False)
    # # value_counts_without_nan = value_counts_with_nan.drop(np.nan, inplace=False)
    # # a = (value_counts_with_nan, value_counts_without_nan, value_counts_with_nan.sum())
    # #
    # pfr = pandas_profiling.ProfileReport(df)
    # pfr.to_file("/tmp/example.html")

    # df = pd.read_csv("../examples/Meteorite_Landings.csv", encoding='UTF-8')
    # # Note: Pandas does not support dates before 1880, so we ignore these for this analysis
    # df['year'] = pd.to_datetime(df['year'], errors='coerce')
    # 
    # # Example: Constant variable
    # df['source'] = "NASA"
    # 
    # # Example: Boolean variable
    # df['boolean'] = np.random.choice([True, False], df.shape[0])
    # 
    # # Example: Boolean variable
    # df['booleanNAN'] = np.random.choice([True, False, np.nan], df.shape[0])
    # 
    # # Example: Boolean variable
    # df['boolean10NAN'] = np.random.choice([1, 0, np.nan], df.shape[0])
    # 
    # # Example: Boolean variable
    # df['boolean10'] = np.random.choice([1, 0], df.shape[0])
    # 
    # # Example: Boolean variable
    # df['booleanYN'] = np.random.choice(["Y", "N"], df.shape[0])
    # 
    # # Example: Boolean variable
    # df['booleanYNNAN'] = np.random.choice(["Y", "N", np.nan], df.shape[0])
    # 
    # # Example: Highly correlated variables
    # df['reclat_city'] = df['reclat'] + np.random.normal(scale=5, size=(len(df)))
    # 
    # # Example: Duplicate observations
    # duplicates_to_add = pd.DataFrame(df.iloc[0:10])
    # duplicates_to_add[u'name'] = duplicates_to_add[u'name'] + " copy"
    # 
    # df = df.append(duplicates_to_add, ignore_index=True)
    # pfr = pandas_profiling.ProfileReport(df)
    # pfr.to_file("/tmp/example.html")

    import datetime

    data = {'id': [chr(97 + c) for c in range(1, 10)],
            'x': [50, 50, -10, 0, 0, 5, 15, -3, None],
            'y': [0.000001, 654.152, None, 15.984512, 3122, -3.1415926535, 111, 15.9, 13.5],
            'cat': ['a', 'long text value', u'Élysée', '', None, 'some <b> B.s </div> </div> HTML stuff', 'c',
                    'c',
                    'c'],
            'cat2': ['a', 'long text value', u'Élysée', '', None, 'some <b> B.s </div> </div> HTML stuff', 'c',
                     'c',
                     'c'],
            'cat3': ['a', 'long text value', u'Élysée', '', None, 'some <b> B.s </div> </div> HTML stuff', 'c',
                     'c',
                     'b'],
            'cat4': ['b', 'some <b> B.s </div> </div> HTML stuff', '', None, 'long text value', u'Élysée', 'c',
                     'c',
                     'a'],
            's1': np.ones(9),
            's2': [u'some constant text $ % value {obj} ' for _ in range(1, 10)],
            'somedate': [datetime.date(2011, 7, 4), datetime.datetime(2011, 7, 7, 13, 57),
                         datetime.datetime(2011, 7, 9), np.nan,
                         datetime.datetime(
                             2011, 7, 7), datetime.datetime(2011, 7, 9),
                         datetime.datetime(2011, 7, 2), datetime.datetime(2011, 7, 9),
                         datetime.datetime(2011, 7, 9)],
            'bool_tf': [True, True, False, True, False, True, True, False, True],
            'bool_tf_with_nan': [True, False, False, False, False, True, True, False, np.nan],
            'bool_01': [1, 1, 0, 1, 1, 0, 0, 0, 1],
            'bool_01_with_nan': [1, 0, 1, 0, 0, 1, 1, 0, np.nan],
            'list': [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]],
            'mixed': [1, 2, "a", 4, 5, 6, 7, 8, 9],
            'dict': [{'a': 'a'}, {'b': 'b'}, {'c': 'c'}, {'d': 'd'}, {'e': 'e'}, {'f': 'f'}, {'g': 'g'}, {'h': 'h'},
                     {'i': 'i'}],
            'tuple': [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 18)]
            }

    df = pd.DataFrame(data)

    df['somedate'] = pd.to_datetime(df['somedate'])

    pfr = pandas_profiling.ProfileReport(df, bins="auto")
    pfr.to_file("/tmp/example.html")