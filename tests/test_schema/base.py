# -*- encoding: utf-8 -*-
"""
    test.schema.base
    ----------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jsonschema
from flask_triangle.schema import Schema

from nose.tools import assert_in, assert_not_in, assert_equal, assert_is, raises


class SanityCheck(object):
    """
    A precheck of basic features.
    """

    def test_item_schema_property(self):
        """
        any item should have a schema property retuning a dict
        """
        assert_is(type(self.item.schema), dict)


class CheckBaseProperties(object):
    """
    Test all base attributes of an item.
    """

    def test_item_has_type(self):
        """
        any item should have a type.
        """
        assert_in('type', self.item.schema)

    def test_item_optional_enum0(self):
        """
        if enum is an empty array or None, item's schema does not have a `enum`
        property.
        """
        assert_not_in('enum', self.item.schema)
        self.item.enum = []
        assert_not_in('enum', self.item.schema)

    def test_item_optional_enum1(self):
        """
        if enum is an empty array or None, item's schema does not have a `enum`
        property.
        """
        self.item.enum = ['some', 'values']
        assert_in('enum', self.item.schema)
        assert_equal(self.item.schema.get('enum'), ['some', 'values'])

    def test_item_optional_allof0(self):
        """
        """
        assert_not_in('allOf', self.item.schema)
        self.item.all_of = []
        assert_not_in('allOf', self.item.schema)

    def test_item_optional_allof1(self):
        """
        """
        self.item.all_of = [Schema()]
        assert_in('allOf', self.item.schema)

    @raises(AttributeError)
    def test_item_optional_allof2(self):
        """
        """
        self.item.all_of = ['not_an_item']
        assert_in('allOf', self.item.schema)

    def test_item_optional_anyof0(self):
        """
        """
        assert_not_in('anyOf', self.item.schema)
        self.item.any_of = []
        assert_not_in('anyOf', self.item.schema)

    def test_item_optional_anyof1(self):
        """
        """
        self.item.any_of = [Schema()]
        assert_in('anyOf', self.item.schema)

    @raises(AttributeError)
    def test_item_optional_anyof2(self):
        """
        """
        self.item.any_of = ['not_an_item']
        self.item.schema

    def test_item_optional_oneof0(self):
        """
        """
        assert_not_in('oneOf', self.item.schema)
        self.item.one_of = []
        assert_not_in('oneOf', self.item.schema)

    def test_item_optional_oneof1(self):
        """
        """
        self.item.one_of = [Schema()]
        assert_in('oneOf', self.item.schema)

    @raises(AttributeError)
    def test_item_optional_oneof2(self):
        """
        """
        self.item.one_of = ['not_an_item']
        self.item.schema

    def test_item_optional_not0(self):
        """
        """
        assert_not_in('not', self.item.schema)

    def test_item_optional_not1(self):
        """
        """
        self.item.is_not = Schema()
        assert_in('not', self.item.schema)

    @raises(AttributeError)
    def test_item_optional_not2(self):
        """
        """
        self.item.is_not = 'not_an_item'
        self.item.schema


class CheckCacheMechanism(object):

    def test_cache_set(self):
        """
        The schema can be cached.
        """
        assert_not_in('enum', self.item.schema)
        self.item.cache()
        self.item.enum = ['some', 'values']
        assert_not_in('enum', self.item.schema)

    def test_cache_unset(self):
        """
        The cache can be unset.
        """
        self.item.cache()
        self.item.enum = ['some', 'values']
        assert_not_in('enum', self.item.schema)
        self.item.cache(False)
        assert_equal(self.item.schema.get('enum'), ['some', 'values'])

    def test_override_schema(self):
        """
        The computed schema can be overridden with a custom schema.
        """
        assert_not_in('properties', self.item.schema)
        self.item.schema = {'type': 'object',
                            'properties': {'custom': {'type': 'boolean'}}}
        assert_in('properties', self.item.schema)
