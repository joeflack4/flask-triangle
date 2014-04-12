# -*- encoding: utf-8 -*-
"""
    helpers.compat
    ---------------

    Helpers to support Python3 along with Python2.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import sys

PY3 = sys.version_info[0] >= 3

if PY3:
    base_str = str
else:
    base_str = unicode
