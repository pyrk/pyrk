# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
PyRK is a point reactor kinetics and thermal hydraulics solver module
for coupled, 0-D transient analysis.
"""
from version import get_git_version

try:
    __version__ = get_git_version()
except (ValueError, IOError):
    __version__ = 'unknown'
