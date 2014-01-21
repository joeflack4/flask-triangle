# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import assert_equal

from flask_triangle.widgets.standard import Select
from flask_triangle.modifiers import Multiple
from flask_triangle.schema import Schema, Object, String

from nose.tools import raises, assert_is_not
import re, jsonschema


class TestMultipleSimpleValidation(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('test', String())

    def test_reference_schema_success(self):
        """
        The reference schema validates a string.
        """
        self.schema.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_reference_schema_fail(self):
        """
        The reference schema fails to validate a list of string.
        """
        self.schema.validate({'test': ['ko0', 'ko1']})

    @raises(jsonschema.ValidationError)
    def test_modified_schema_fail0(self):
        """
        The modified schema fails to validate a string.
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': 'ko'})

    def test_modified_schema_success(self):
        """
        The modified schema validates a list of string.
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['ok0', 'ok1']})

    @raises(jsonschema.ValidationError)
    def test_modified_schema_fail1(self):
        """
        The modified schema fails to validate a list with invalid data.
        (i.e. not a string value in the test context.)
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['ok', 0]})

    @raises(jsonschema.ValidationError)
    def test_option_unique_fail(self):
        """
        If two values are identical in the the validation fails.
        """
        modifier = Multiple(unique_items=True)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['ok', 'ok']})

    def test_option_unique_success(self):
        """
        If two values are identical in the the validation fails.
        """
        modifier = Multiple(unique_items=True)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['ok0', 'ok1']})

    @raises(jsonschema.ValidationError)
    def test_option_min_items_fail(self):
        """
        If there is not enough items, the validation fails.
        """
        modifier = Multiple(min_items=2)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['fail']})

    def test_option_min_items_success(self):
        """
        If there is not enough items, the validation fails.
        """
        modifier = Multiple(min_items=2)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['is', 'successfull']})

    @raises(jsonschema.ValidationError)
    def test_option_max_items_fail(self):
        """
        If there is too much items, the validation fails.
        """
        modifier = Multiple(max_items=2)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['fail', 'fail', 'fail']})

    def test_option_max_items_success(self):
        """
        If there is not too much items, the validation succeed.
        """
        modifier = Multiple(max_items=2)
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': ['is', 'successfull']})


class TestMultipleNestedValidation(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('nested', Object(additional_properties=False))
        self.schema.get('nested').properties.add('value', String())

    def test_reference_schema_success(self):
        """
        The reference schema validates a string.
        """
        self.schema.validate({'nested': {'value': 'ok'}})

    @raises(jsonschema.ValidationError)
    def test_reference_schema_fail(self):
        """
        The reference schema fails to validate a list of string.
        """
        self.schema.validate({'nested': {'value': ['ko0', 'ko1']}})

    @raises(jsonschema.ValidationError)
    def test_modified_schema_fail0(self):
        """
        The modified schema fails to validate a string.
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': 'ko'}})

    def test_modified_schema_success(self):
        """
        The modified schema validates a list of string.
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['ok0', 'ok1']}})

    @raises(jsonschema.ValidationError)
    def test_modified_schema_fail1(self):
        """
        The modified schema fails to validate a list with invalid data.
        (i.e. not a string value in the test context.)
        """
        modifier = Multiple()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['ok', 0]}})

    @raises(jsonschema.ValidationError)
    def test_option_unique_fail(self):
        """
        If two values are identical in the the validation fails.
        """
        modifier = Multiple(unique_items=True)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['ok', 'ok']}})

    def test_option_unique_success(self):
        """
        If two values are identical in the the validation fails.
        """
        modifier = Multiple(unique_items=True)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['ok0', 'ok1']}})

    @raises(jsonschema.ValidationError)
    def test_option_min_items_fail(self):
        """
        If there is not enough items, the validation fails.
        """
        modifier = Multiple(min_items=2)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['fail']}})

    def test_option_min_items_success(self):
        """
        If there is not enough items, the validation fails.
        """
        modifier = Multiple(min_items=2)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['is', 'successfull']}})

    @raises(jsonschema.ValidationError)
    def test_option_max_items_fail(self):
        """
        If there is too much items, the validation fails.
        """
        modifier = Multiple(max_items=2)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['fail', 'fail', 'fail']}})

    def test_option_max_items_success(self):
        """
        If there is not too much items, the validation succeed.
        """
        modifier = Multiple(max_items=2)
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': ['is', 'successfull']}})


class TestMultipleWidget(object):

    def setup(self):
        self.widget = Select('nested.value',
                             options=[],
                             modifiers=[Multiple()])

    def test_rendering(self):
        assert_is_not((re.match('^<select( .*)? multiple( .*)?>.*$', self.widget())), None)

