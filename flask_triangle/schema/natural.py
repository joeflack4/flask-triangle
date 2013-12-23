# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.natural
    -----------------------------

    Include all the primitive types as defined in the JSON schema draft and
    which aren't container type (i.e. Object or Array).

    http://tools.ietf.org/html/draft-zyp-json-schema-04

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .base import BaseType


class Boolean(BaseType):
    """
    """

    def __init__(self, **kwargs):
        super(Boolean, self).__init__('boolean', **kwargs)


class Numeric(BaseType):
    """
    """

    def __init__(self, type_, multiple_of=None, minimum=None, maximum=None,
                 exclusive_maximum=False, exclusive_minimum=False, **kwargs):
        super(Numeric, self).__init__(type_, **kwargs)
        self.multiple_of = multiple_of
        self.maximum = maximum
        self.minimum = minimum
        self.exclusive_maximum = exclusive_maximum
        self.exclusive_minimum = exclusive_minimum

    def __schema__(self):
        """
        Append the specific attributes of the String to the JSON schema.
        """

        res = super(Numeric, self).__schema__()

        if self.multiple_of is not None: res['multipleOf'] = self.multiple_of
        if self.maximum is not None:
            res['maximum'] = self.maximum
            if self.exclusive_maximum:
                res['exclusiveMaximum'] = True
        if self.minimum is not None:
            res['minimum'] = self.minimum
            if self.exclusive_minimum:
                res['exclusiveMinimum'] = True

        return res


class Integer(Numeric):
    """
    """

    def __init__(self, **kwargs):
        super(Integer, self).__init__('integer', **kwargs)


class Number(Numeric):
    """
    """

    def __init__(self, **kwargs):
        super(Number, self).__init__('number', **kwargs)


class String(BaseType):
    """
    """

    def __init__(self, min_length=0, max_length=None, pattern=None, **kwargs):
        super(String, self).__init__('string', **kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern

    def __schema__(self):
        """
        Append the specific attributes of the String to the JSON schema.
        """

        res = super(String, self).__schema__()

        if self.min_length: res['minLength'] = self.min_length
        if self.max_length is not None: res['maxLength'] = self.max_length
        if self.pattern is not None: res['pattern'] = self.pattern

        return res