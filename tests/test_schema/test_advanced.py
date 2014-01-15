# -*- encoding: utf-8 -*-
"""
    test.schema.advanced
    --------------------

    Test advanced features of the json-schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jsonschema

from nose.tools import assert_equal, assert_not_equal
from flask_triangle.schema import Schema, Object, String


class TestComparison(object):
    """
    Execute all the base comparison tests.
    """
    def setup(self):
        self.schema0 = Schema()
        self.schema0.properties.add('value', String())

    def test_equal(self):
        schema1 = Schema()
        schema1.properties.add('value', String())
        assert_equal(schema1, self.schema0)

    def test_not_equal0(self):
        schema1 = Schema()
        schema1.properties.add('other', String())
        assert_not_equal(schema1, self.schema0)

    def test_not_equal1(self):
        schema1 = Schema()
        schema1.properties.add('value', String())
        schema1.properties.add('other', String())
        assert_not_equal(schema1, self.schema0)


class TestIteration0(object):
    """
    Execute the iteration test.
    """

    def setup(self):
        self.schema = Schema()
        nested = Object()
        nested.properties.add('value0', String())
        nested.properties.add('value1', String())
        self.schema.properties.add('nested', nested)
        self.schema.properties.add('value2', String())

    def test_iter_node(self):
        assert_equal(len(list(self.schema)), 5)

    #TODO: improve that !
