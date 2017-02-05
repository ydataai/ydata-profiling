import os

__location__ = os.path.dirname(__file__)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pandas-profiling',
    version='1.4.0',
    author='Jos Polfliet',
    author_email='jos.polfliet+panpro@gmail.com',
    packages=['pandas_profiling'],
    url='http://github.com/jospolfliet/pandas-profiling',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'

    ],
    keywords='pandas data-science data-analysis python jupyter ipython',

)
