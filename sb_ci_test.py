import pandas_profiling as ppf
from pandas_profiling import tests
import pdb
import numpy as np

np.random.seed(96094)

print('BRO U DUMB AF ASK RANDY HOW TO DO THIS FOR REAL FAM')

try:
    try:
        dft = tests.DataFrameTest()
    except:
        tests.DataFrameTest.runTest = lambda x: 'fuk py2'
        dft = tests.DataFrameTest()

    dft.setUp()
    dft.df['yy'] = np.random.randint(2, size=dft.df.shape[0])

    stupid_temp = '/tmp/lol.html'
    stupid_temp2 = '/tmp/lol2.html'

    # run once with all the extras
    profz = ppf.ProfileReport(dft.df, y='yy', corr_threshold=69, ft_names={'x': 'Yeezusss'})

    profz.to_file(stupid_temp)

    # run with just the base parameters
    profz = ppf.ProfileReport(dft.df)
    profz.to_file(stupid_temp2)

    print('=' * 50)
    print(stupid_temp)
    print(stupid_temp2)
except Exception as e:
    print(e)
    pdb.set_trace()
