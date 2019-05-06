import os

__location__ = os.path.dirname(__file__)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandas-profiling',
    version='1.4.2',
    author='Jos Polfliet',
    author_email='jos.polfliet+panpro@gmail.com',
    packages=['dask_profiling'],
    url='https://github.com/pandas-profiling/pandas-profiling',
    license='MIT',
    description='Generate profile report for pandas DataFrame',
    install_requires=[
        "pandas>=0.19",
        "matplotlib>=1.4",
        "jinja2>=2.8",
        "six>=1.9"
    ],
    include_package_data = True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Framework :: IPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'

    ],
    keywords='pandas data-science data-analysis python jupyter ipython',
    long_description=long_description,
    long_description_content_type='text/markdown'

)
