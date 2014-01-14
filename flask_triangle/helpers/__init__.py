# -*- encoding: utf-8 -*-
"""
    helpers
    -------

    A collection of useful things for internal use.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from .python3 import PY3
from .html import HTMLString, camel_to_dash, make_attr


__all__ = ['PY3', 'HTMLString', 'camel_to_dash', 'make_attr']
