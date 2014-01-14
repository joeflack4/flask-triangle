# -*- encoding: utf-8 -*-
"""
    test.widget.schema
    ------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget
from flask_triangle.schema import String

import jsonschema
from nose.tools import assert_equal, raises, assert_in


class CustomWidget0(Widget):
    """
    A custom widget.
    """
    schema = String()
    html_template = '<input {{attr}}>Valid HTML</input>'


class TestWidgetSchema0(object):

    def setup(self):
        self.widget = CustomWidget0('test')

    def test0(self):
        """
        the ng-value is binded to a json schema property.
        """
        assert_in('test', self.widget.schema.schema['properties'])

    def test1(self):
        """
        the type of the property is the expected one.
        """
        assert_equal('string',
                     self.widget.schema.schema['properties']['test']['type'])

    def test2(self):
        """
        the schema is valid.
        """
        jsonschema.Draft4Validator.check_schema(self.widget.schema.schema)

    def test3(self):
        """
        the schema validate a valid value.
        """
        self.widget.schema.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test4(self):
        """
        the schema raises an error for an invalid input.
        """
        self.widget.schema.validate({'test': 0})


class TestWidgetSchema1(object):

    def setup(self):
        """
        """
        self.widget = CustomWidget0('this.is.a.test')

    def test0(self):
        """
        test the nested construction of the schema.
        """
        assert_in('this', self.widget.schema.schema['properties'])
        assert_in('is',
                  self.widget.schema.schema['properties']['this']['properties'])
        assert_in('a',
                  self.widget.schema.schema['properties']['this']['properties']['is']['properties'])
        assert_in('test',
                  self.widget.schema.schema['properties']['this']['properties']['is']['properties']['a']['properties'])

    def test1(self):
        """
        """
        assert_equal('string',
                     self.widget.schema.schema['properties']['this']['properties']['is']['properties']['a']['properties']['test']['type'])

    def test2(self):
        """
        the schema is valid.
        """
        jsonschema.Draft4Validator.check_schema(self.widget.schema.schema)

    def test3(self):
        """
        the schema validate a valid value.
        """
        self.widget.schema.validate({'this': {'is': {'a': {'test': 'ok'}}}})

    @raises(jsonschema.ValidationError)
    def test4(self):
        """
        the schema raises an error for an invalid input.
        """
        self.widget.schema.validate({'this': {'is': {'a': {'test': 0}}}})
