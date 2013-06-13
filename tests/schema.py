# -*- encoding: utf-8 -*-
"""
    test.schema
    -----------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from flask_triangle.schema import Schema

from nose.tools import assert_true, assert_equal, assert_in, assert_not_in
import mock


class TestSchema0(object):

    def setup(self):
        pass

    def test_type(self):
        """Schema is a dict"""
        assert_true(issubclass(Schema, dict))

    def test_init0(self):
        """The default schema is an empty dict"""
        assert_equal(len(Schema()), 0)

    def test_init1(self):
        """A Schema can be initialized with an existing dict"""
        schema = Schema({u'test': u'ok'})
        assert_equal(len(schema), 1)
        assert_in(u'test', schema)
        assert_equal(schema[u'test'], u'ok')


class TestSchema1(object):

    def setup(self):
        """call a function on each subschema."""

        self.func_nobreak = mock.Mock(return_value=False)
        self.func_break = mock.Mock(return_value=True)

    def test_apply_func0(self):
        """the applied func is called on the root and each properties"""
        schema = Schema({u'type': u'object',
                          u'properties': {u'first': Schema({u'type': u'string'}),
                                          u'last': Schema({u'type': u'string'})}})

        schema.apply_func(self.func_nobreak)

        expected = [mock.call(schema, u''),
                    mock.call(schema[u'properties'][u'last'], u'last'),
                    mock.call(schema[u'properties'][u'first'], u'first')]
        assert_equal(self.func_nobreak.call_args_list, expected)

    def test_apply_func1(self):
        """
        the applied func is called on the root only if the function breaks the
        process by returning a non-false value.
        """
        schema = Schema({u'type': u'object',
                          u'properties': {u'first': Schema({u'type': u'string'}),
                                          u'last': Schema({u'type': u'string'})}})

        schema.apply_func(self.func_break)

        expected = [mock.call(schema, u'')]
        assert_equal(self.func_break.call_args_list, expected)

    def test_apply_func2(self):
        """
        the applied func is called on nested properties.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'parent': Schema({u'type': u'object',
                                                            u'properties': {u'child': Schema({u'type': u'string'})}})}})

        schema.apply_func(self.func_nobreak)

        expected = [mock.call(schema, u''),
                    mock.call(schema[u'properties'][u'parent'], u'parent'),
                    mock.call(schema[u'properties'][u'parent'][u'properties'][u'child'], u'parent.child')]
        assert_equal(self.func_nobreak.call_args_list, expected)

    def test_apply_func3(self):
        """
        the applied func is called for pattern proterties but use a '*' token.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'named': Schema({u'type': u'string'})},
                         u'patternProperties': {u'^(/[^/]+)+$': Schema({u'type': u'string'})}})

        schema.apply_func(self.func_nobreak)

        expected = [mock.call(schema, u''),
                    mock.call(schema[u'properties'][u'named'], u'named'),
                    mock.call(schema[u'patternProperties'][u'^(/[^/]+)+$'], u'*')]
        assert_equal(self.func_nobreak.call_args_list, expected)


class TestSchema2(object):

    def test_0(self):
        """
        A property with a 'asPatternProperty' key convert a named property to
        a pattenProperty using the value of 'asPatternProperty' as pattern. 
        This property is removed from the patternProperty
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'normal': Schema({u'type': u'string'}),
                                         u'pattern': Schema({u'type': u'string',
                                                             u'asPatternProperty': u'^(/[^/]+)+$'})}})

        schema.compile()
        assert_not_in(u'pattern', schema[u'properties'])
        assert_not_in(u'pattern', schema[u'patternProperties'])
        assert_in(u'^(/[^/]+)+$', schema[u'patternProperties'])
        assert_not_in(u'asPatternProperty', schema[u'patternProperties'][u'^(/[^/]+)+$'])

    def test_1(self):
        """
        If the property was in the required list before being moved to
        patternProperties, its name is removed.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'normal': Schema({u'type': u'string'}),
                                         u'pattern': Schema({u'type': u'string',
                                                             u'asPatternProperty': u'^(/[^/]+)+$'})},
                         u'required': [u'pattern', u'normal']})

        schema.compile()
        assert_not_in(u'pattern', schema[u'required'])

    def test_2(self):
        """
        If the required list is empty after the removal of value, the required
        field is also removed.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'normal': Schema({u'type': u'string'}),
                                         u'pattern': Schema({u'type': u'string',
                                                             u'asPatternProperty': u'^(/[^/]+)+$'})},
                         u'required': [u'pattern']})

        schema.compile()
        assert_not_in(u'required', schema)

    def test_3(self):
        """
        If there is no more properties in the obhect, this field is removed.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'pattern': Schema({u'type': u'string',
                                                             u'asPatternProperty': u'^(/[^/]+)+$'})}})

        schema.compile()
        assert_not_in(u'properties', schema)

    def test_4(self):
        """
        If there is already patterProperties the list is appended.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'pattern': Schema({u'type': u'string',
                                                             u'asPatternProperty': u'^(/[^/]+)+$'})},
                         u'patternProperties': {u'^[A-Z]*$': Schema({u'type': u'string'})}})

        assert_equal(len(schema[u'patternProperties']), 1)
        schema.compile()
        assert_equal(len(schema[u'patternProperties']), 2)


class TestSchema3(object):

    def setup(self):

        self.schema = Schema({'a': 5,
                              'b': 6,
                              'c': [0, 1, 2, 3],
                              'd': {'a': 5,
                                    'b': 6,
                                    'c': [0, 1, 2, 3]}})

    def test_0(self):
        """Merging two Schemas with no intersection complete the first one."""

        self.schema.merge(Schema({'e': 10}))
        assert_equal(len(self.schema), 5)
        assert_in('e', self.schema)

    def test_1(self):
        """
        Merging two Schemas with an intersection on a key will update this key
        if the key is not a mapping or a list.
        """

        self.schema.merge(Schema({'b': 10}))
        assert_equal(len(self.schema), 4)
        assert_equal(self.schema['b'], 10)

    def test_2(self):
        """
        Merging two Schemas with an intersection on a key will update this key
        if the associated values are not of the same kind.
        """

        self.schema.merge(Schema({'c': 10}))
        assert_equal(len(self.schema), 4)
        assert_equal(self.schema['c'], 10)

    def test_3(self):
        """
        Merging two Schemas with an intersection on a key and both of the value
        are of list type will merge them together.
        """

        self.schema.merge(Schema({'c': [10]}))
        assert_equal(len(self.schema), 4)
        assert_equal(sorted(self.schema['c']), [0, 1, 2, 3, 10])

    def test_4(self):
        """
        Merging two Schemas with an intersection on a key and both of the value
        are of list type will merge them together but will drop duplicate.
        """

        self.schema.merge(Schema({'c': [3]}))
        assert_equal(len(self.schema), 4)
        assert_equal(sorted(self.schema['c']), [0, 1, 2, 3])

    def test_5(self):
        """
        The merge method is recursive when both key are mapping collections
        """
        #TODO: despite it works, I must found a way to really test the
        #      recursive method implied in the merging process.
        self.schema.merge(Schema({'d': {'e': 10}}))
        assert True
