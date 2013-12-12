# -*- encoding: utf-8 -*-
"""
    flask_triangle.helpers.html
    ---------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from . import PY3


# Python3 support.
base = str
if not PY3:
    base = unicode


class HTMLString(base):
    """
    HTMLString is a special string object with an __html__ method used by Jinja2
    to render the text as safe HTML code.
    """

    def __html__(self):
        return self
