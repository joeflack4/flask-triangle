# -*- encoding: utf-8 -*-
"""
    tests.widgets.widget
    --------------------

    Test the widget base class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle.widgets.base import Widget
from nose.tools import assert_equal, assert_not_in, assert_in
from jsonschema import Draft3Validator
from flask_triangle.validators.base import Validator

import mock


Widget.json_type = 'test'
Widget.html_template = '<input {attributes}/>'


class TestWidgetInit(object):

    def test_binding(self):
        """
        The binding value is stored as the `ng-model` attribute of the HTML
        widget.
        """
        widget = Widget('test')
        assert_equal(widget.attributes.get('ng-model'), 'test')

    def test_name(self):
        """The name is stored as the `name` attribute of the HTML widget."""
        widget = Widget('test', name='name')
        assert_equal(widget.attributes.get('name'), 'name')

    def test_attribute_priority(self):
        """A user set attribute always takes priority over generated ones."""
        widget = Widget('test', name='drop', html_attributes={'name': 'ok'})
        assert_equal(widget.attributes.get('name'), 'ok')


class TestWidgetProperties(object):

    def setup(self):
        self.widget0 = Widget('binding', name='name')
        self.widget1 = Widget('binding', name='name', label='label')

    def test_name_0(self):
        """name is accessible through a property"""
        assert_equal(self.widget0.name, self.widget0.attributes.get('name'))

    def test_name_1(self):
        """setting name through the property update the attribute."""
        self.widget0.name = 'valid'
        assert_equal(self.widget0.attributes.get('name'), 'valid')

    def test_label_0(self):
        """label is accessible through a property."""
        assert_equal(self.widget1.label, 'label')

    def test_label_1(self):
        """
        If no label has been set the label properties return the name value.
        """
        assert_equal(self.widget0.label, 'name')

    def test_label_2(self):
        """Set the label when not set does not affect the name property."""
        self.widget0.label = 'label'
        assert_equal(self.widget0.label, 'label')
        assert_equal(self.widget0.name, 'name')



class TestWidgetSchema(object):

    def setup(self):
        self.widget0 = Widget('test')
        self.widget1 = Widget('nested.test')

    def test_0(self):
        """The root of the validation schema is from `object` type."""
        assert_equal(self.widget0.schema['type'], 'object')

    def test_1(self):
        """Convert binding name to property of the root object"""
        assert_in('test', self.widget0.schema['properties'])

    def test_2(self):
        """
        Binding of nested object is expressed with dot as in javascript and
        is reflected in the schema.
        """
        nested_schema = self.widget1.schema['properties']['nested']
        assert_in('test', nested_schema['properties'])

    def test_3(self):
        """The leaf object is of the defined type."""
        assert_equal(self.widget0.schema['properties']['test']['type'],
                     self.widget0.json_type)

    def test_valid_schema(self):
        """A schema with simple binding is valid."""
        Draft3Validator.check_schema(self.widget0.schema)

    def test_valid_nested_schema(self):
        """A schema with nested binding is valid."""
        Draft3Validator.check_schema(self.widget1.schema)


class TestWidgetValidator(object):

    def setup(self):
        self.val = Validator()
        self.val.attributes = {'val_attr': 'ok'}
        self.val.alter_schema = mock.Mock(return_value=True)
        self.widget = Widget('bind', validators=[self.val])

    def test_alter_schema(self):
        """
        The constructor call the alter_schema method of each validators at
        least once.
        """
        self.val.alter_schema.assert_called_once()
