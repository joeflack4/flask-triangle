# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import raises

from flask_triangle.modifiers import AsBoolean, AsInteger
from flask_triangle.schema import Schema, String

import jsonschema


class TestAsBoolean(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('test', String())

    @raises(jsonschema.ValidationError)
    def test_ref_fail(self):
        """
        """
        self.schema.validate({'test': False})

    def test_ref_success(self):
        self.schema.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_mod_fail(self):
        modifier = AsBoolean()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': 'ok'})

    def test_mod_success(self):
        modifier = AsBoolean()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': False})

class TestAsInteger(object):

    def setup(self):
        # setup a reference schema
        self.schema = Schema(additional_properties=False)
        self.schema.properties.add('test', String())

    @raises(jsonschema.ValidationError)
    def test_ref_fail(self):
        """
        """
        self.schema.validate({'test': 1})

    def test_ref_success(self):
        self.schema.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_mod_fail(self):
        modifier = AsInteger()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': 'ok'})

    def test_mod_success(self):
        modifier = AsInteger()
        modifier.alter_schema(self.schema, 'test')
        self.schema.validate({'test': 1})
