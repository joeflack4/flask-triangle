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
from flask_triangle.schema import Array, String

from nose.tools import assert_equal, assert_in, assert_not_in


class TestString(SanityCheck, CheckBaseProperties, CheckCacheMechanism):
    """
    Execute all the base tests.
    """

    def setup(self):
        self.item = Array(String())

    def test_max_length(self):
        self.item.max_items = 2
        assert_in('maxItems', self.item.schema)
        assert_equal(self.item.schema['maxItems'], 2)

    def test_min_length(self):
        self.item.min_items = 2
        assert_in('minItems', self.item.schema)
        assert_equal(self.item.schema['minItems'], 2)

    def test_unique_items(self):
        self.item.unique_items = True
        assert_in('uniqueItems', self.item.schema)
        assert_equal(self.item.schema['uniqueItems'], True)