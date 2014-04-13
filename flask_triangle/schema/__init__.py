# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema
    ---------------------

    A set of tools to manage a JSON Schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .containers import Schema, Object, Array
from .natural import Boolean, Integer, Number, String


__all__ = [
    'Schema', 'Object', 'Boolean', 'Integer', 'Number', 'String', 'Array',
]
