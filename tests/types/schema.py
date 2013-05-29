# -*- encoding: utf-8 -*-


from flask_triangle.types import Schema
from nose.tools import assert_true, assert_in, assert_equal


class TestSchema(object):

    def test_schema_type(self):
        """Schema is a dict."""
        assert_true(issubclass(Schema, dict))

    def test_update_as_union(self):
        """
        Update a schema with an non-intersecting one will make the former as
        an union of the two.
        """
        schema0 = Schema({'a': True})
        schema1 = Schema({'b': True})

        schema0.update(schema1)

        assert_in('a', schema0)
        assert_in('b', schema0)

    def test_update_as_replace(self):
        """
        Updating an existing key in a schema will replace its former value with
        the new one.
        """
        schema0 = Schema({'a': False})
        schema1 = Schema({'a': True})

        schema0.update(schema1)

        assert_equal(schema0.get('a'), True)

    def test_update_subdict(self):
        """
        Updating an existing key in a schema will update its value if it is a
        dict type.
        """

        schema0 = Schema({'a': {'c': True}})
        schema1 = Schema({'a': {'b': True}})

        schema0.update(schema1)

        assert_in('c', schema0.get('a'))
        assert_in('b', schema0.get('a'))

    def test_update_list(self):
        """
        Updating an existing key in a schema will merge its value if it is a
        list type and remove duplicates.
        """

        schema0 = Schema({'a': [0, 1]})
        schema1 = Schema({'a': [1, 2]})

        schema0.update(schema1)

        assert_equal(len(schema0.get('a')), 3)
        assert_in(0, schema0.get('a'))
        assert_in(1, schema0.get('a'))
        assert_in(2, schema0.get('a'))
