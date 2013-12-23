# -*- encoding: utf-8 -*-
"""
    flask_triangle.exc
    ------------------

    A collection of exceptions.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


class MergeError(RuntimeError):
    """
    This error is raised when the merge of two JSON Schemas is impossible.
    """
    pass