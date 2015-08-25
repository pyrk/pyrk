from __future__ import print_function
from setuptools import setup
import io
import os

import pyrk
#from version import get_git_version

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CONTRIBUTING.md')

setup(
    name='pyrk',
    #version=get_git_version(),
    url='http://github.com/katyhuff/pyrk/',
    license='BSD 3-Clause License',
    author='Kathryn D. Huff',
    tests_require=['nose'],
    author_email='katyhuff@gmail.com',
    description='Transient Neutron Kinetics Simulation in 0D.',
    long_description=long_description,
    packages=['pyrk','pyrk.utils','pyrk.materials','pyrk.inp'],
    include_package_data=True,
    platforms='any',
    test_suite='pyrk.test.test_pyrk',
    classifiers=[
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
