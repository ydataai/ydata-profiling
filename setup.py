try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pandas-profiling',
    version='0.1.0',
    author='Jos Polfliet',
    author_email='jos.polfliet+panpro@gmail.com',
    packages=['pandas_profiling'],
    url='http://github.com/jospolfliet/pandas-profiling',
    license='LICENSE',
    description='Generate profile report for pandas DataFrame',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas",
        "matplotlib"
    ],
)