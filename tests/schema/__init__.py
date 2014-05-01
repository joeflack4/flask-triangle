# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from .object import TestObjectProperties, TestObjectFeatures
from .natural import TestString, TestInteger, TestNumber, TestBoolean


__all__ = [
    'TestObjectProperties',
    'TestObjectFeatures',
    'TestString',
    'TestInteger',
    'TestNumber',
    'TestBoolean'
]
