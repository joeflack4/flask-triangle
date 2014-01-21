# -*- encoding: utf-8 -*-
"""
    tests.validators.required
    -------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import raises

from flask_triangle.modifiers import Required
from flask_triangle.schema import Schema, Object, String

import jsonschema


class TestRootRequired(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('test', String())

    def test_ref_success(self):
        """
        The property test is not required.
        """
        self.schema.validate({})

    @raises(jsonschema.ValidationError)
    def test_mod_fail(self):
        """
        The property test is required.
        """
        modifier = Required()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({})

    def test_mod_success(self):
        """
        The property test is required.
        """
        modifier = Required()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': 'ok'})


class TestNestedRequired(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('nested', Object(additional_properties=False))
        self.schema.get('nested').properties.add('value', String())

    def test_ref_success(self):
        """
        """
        self.schema.validate({})

    @raises(jsonschema.ValidationError)
    def test_mod_fail0(self):
        """
        """
        modifier = Required()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({})

    @raises(jsonschema.ValidationError)
    def test_mod_fail1(self):
        """
        """
        modifier = Required()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {}})

    def test_mod_success(self):
        """
        """
        modifier = Required()
        modifier.alter_schema(self.schema, 'nested.value')
        self.schema.validate({'nested': {'value': 'success'}})
