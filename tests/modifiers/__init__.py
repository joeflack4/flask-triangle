# -*- encoding: utf-8 -*-
"""
    tests.modifiers
    ---------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from .limits import TestLengthLimitsMin, TestLengthLimitsMax
from .required import TestRequired
from .patterns import TestRegexp
from .strict import TestStrict


__all__ = [
    'TestRequired',
    'TestLengthLimitsMin',
    'TestLengthLimitsMax',
    'TestRegexp',
    'TestStrict'
]
