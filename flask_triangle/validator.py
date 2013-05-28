# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""

from __future__ import absolute_import

from .types import Attributes


class Validator(object):
    """The base class for all validators"""

    def __init__(self):
        self.attributes = Attributes()
        self.schema_validator = {}
