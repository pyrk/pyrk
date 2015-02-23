# Licensed under a 3-clause BSD style license - see LICENSE
"""
This module contains errors/exceptions and warnings needed globally in the prke
module. Subclass-specific exceptions should appear in their own subclass
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class prkeWarning(Warning):
    """
    The base warning class from which all prke warnings should inherit.
    """
