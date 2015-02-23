from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import prke

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md','CONTRIBUTING.md')

setup(
    name='prke',
    version=prke.__version__,
    url='http://github.com/katyhuff/prke/',
    license='BSD 3-Clause License',
    author='Jeff Knupp',
    tests_require=['nose'],
    author_email='katyhuff@gmail.com',
    description='Automated REST APIs for existing database-driven systems',
    long_description=long_description,
    packages=['prke'],
    include_package_data=True,
    platforms='any',
    test_suite='prke.test.test_prke',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    extras_require={
        'testing': ['nose'],
    }
)
