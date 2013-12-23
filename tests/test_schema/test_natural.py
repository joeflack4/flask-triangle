# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .base import SanityCheck, CheckBaseProperties, CheckCacheMechanism
from flask_triangle.schema import String, Boolean, Integer, Number

from nose.tools import assert_equal, assert_in, assert_not_in


class TestBoolean(SanityCheck, CheckBaseProperties, CheckCacheMechanism):
    """
    Execute all the base tests.
    """

    def setup(self):
        self.item = Boolean()


class TestString(SanityCheck, CheckBaseProperties, CheckCacheMechanism):
    """
    Execute all the base tests.
    """

    def setup(self):
        self.item = String()

    def test_max_length(self):
        self.item.max_length = 2
        assert_in('maxLength', self.item.schema)
        assert_equal(self.item.schema['maxLength'], 2)

    def test_min_length(self):
        self.item.min_length = 2
        assert_in('minLength', self.item.schema)
        assert_equal(self.item.schema['minLength'], 2)

    def test_pattern(self):
        self.item.pattern = '^test$'
        assert_in('pattern', self.item.schema)
        assert_equal(self.item.schema['pattern'], '^test$')


class CheckNumeric(SanityCheck, CheckBaseProperties, CheckCacheMechanism):
    """
    Common tests to all numerics (Integer and Number)
    """
    def test_maximum(self):
        """
        A numeric can have a maximum value.
        """
        self.item.maximum = 2
        assert_in('maximum', self.item.schema)
        assert_equal(self.item.schema['maximum'], 2)

    def test_exclusive_maximum(self):
        """
        A numeric can have an exclusive maximum value by setting
        exclusive_maximum to True and the maximum attributes.
        """
        self.item.maximum = 2
        self.item.exclusive_maximum = True
        assert_in('maximum', self.item.schema)
        assert_equal(self.item.schema['maximum'], 2)
        assert_in('exclusiveMaximum', self.item.schema)
        assert_equal(self.item.schema['exclusiveMaximum'], True)

    def test_exclusive_maximum_precond(self):
        """
        Exclusive_maximum requires a maximum value.
        """
        self.item.exclusive_maximum = True
        assert_not_in('exclusiveMaximum', self.item.schema)

    def test_minimum(self):
        """
        A numeric can have a minimum value.
        """
        self.item.minimum = 2
        assert_in('minimum', self.item.schema)
        assert_equal(self.item.schema['minimum'], 2)

    def test_exclusive_minimum(self):
        """
        A numeric can have an exclusive minimum value by setting
        exclusive_minimum to True and the minimum attributes.
        """
        self.item.minimum = 2
        self.item.exclusive_minimum = True
        assert_in('minimum', self.item.schema)
        assert_equal(self.item.schema['minimum'], 2)
        assert_in('exclusiveMinimum', self.item.schema)
        assert_equal(self.item.schema['exclusiveMinimum'], True)

    def test_exclusive_minimum_precond(self):
        """
        Exclusive_minimum requires a minimum value.
        """
        self.item.exclusive_minimum = True
        assert_not_in('exclusiveMinimum', self.item.schema)


class TestInteger(CheckNumeric):
    """
    """

    def setup(self):
        self.item = Integer()


class TestNumber(CheckNumeric):
    """
    """

    def setup(self):
        self.item = Number()
