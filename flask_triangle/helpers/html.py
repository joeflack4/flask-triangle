# -*- encoding: utf-8 -*-
"""
    flask_triangle.helpers.html
    ---------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import re
from . import PY3


# Python3 support.
string = str
if not PY3:
    string = unicode


def camel_to_dash(value):
    """
    Convert camel-case notation to dash separated. This method is useful for
    HTML attribute generation from keyword arguments.
    """
    if re.match(r'^[A-Za-z0-9]+$', value):
        words = re.split(r'(^[a-z]*)|([A-Z][^A-Z]+)', value)
        return '-'.join(c for c in words if c is not None and c).lower()
    return value.lower()


def make_attr(key, value):
    """
    Convert a key value pair to a valid html attribute.
    It supports AngularJS expression as value with the use of the '|angular'
    suffix.
    """
    if value is None:
        return camel_to_dash(key)
    else:
        value = string(value)
        if value is bool: value = value.lower()
        if value.endswith('|angular'):
            value = '{{{{{{{{{}}}}}}}}}'.format(value[:-8])
        return '{}="{}"'.format(camel_to_dash(key), value)


class HTMLString(string):
    """
    HTMLString is a special string object with an __html__ method used by Jinja2
    to render the text as safe HTML code.
    """

    def __html__(self):
        return self
