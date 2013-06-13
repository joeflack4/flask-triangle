# -*- encoding: utf-8 -*-
"""


"""


from flask_triangle.widget import Widget
from nose.tools import assert_equal, assert_not_in, assert_in
from jsonschema import Draft3Validator
from flask_triangle.validator import Validator

import mock


class TestWidgetConstructor(object):

    def setup(self):
        pass

    def test_binding(self):
        """
        The binding value is stored as the `ng-model` attribute of the HTML
        widget.
        """
        widget = Widget(u'test')
        assert_equal(widget.attributes.get(u'ng-model'), u'test')

    def test_name(self):
        """The name is stored as the `name` attribute of the HTML widget."""
        widget = Widget(u'test', name=u'name')
        assert_equal(widget.attributes.get(u'name'), u'name')

    def test_kwarg(self):
        """
        Keyword arguments are added as attributes by using them as key-value
        pairs. Angular's ngProperties are switched from camel-case to dashed
        notation.
        """
        widget = Widget(u'binding', test=u'valid0', ngTest=u'valid1')
        assert_in('test', widget.attributes)
        assert_equal(widget.attributes.get(u'test'), u'valid0')

        assert_not_in(u'ngTest', widget.attributes)
        assert_in(u'ng-test', widget.attributes)
        assert_equal(widget.attributes.get(u'ng-test'), u'valid1')

class TestWidgetProperties(object):

    def setup(self):
        self.widget0 = Widget(u'binding', name=u'name')
        self.widget1 = Widget(u'binding', name=u'name', label=u'label')

    def test_name_0(self):
        """name is accessible through a property"""
        assert_equal(self.widget0.name, self.widget0.attributes.get(u'name'))

    def test_name_1(self):
        """setting name through the property update the attribute."""
        self.widget0.name = u'valid'
        assert_equal(self.widget0.attributes.get(u'name'), u'valid')

    def test_label_0(self):
        """label is accessible through a property."""
        assert_equal(self.widget1.label, u'label')

    def test_label_1(self):
        """
        If no label has been set the label properties return the name value.
        """
        assert_equal(self.widget0.label, u'name')

    def test_label_2(self):
        """Set the label when not set does not affect the name property."""
        self.widget0.label = u'label'
        assert_equal(self.widget0.label, u'label')
        assert_equal(self.widget0.name, u'name')

class TestWidgetSchema(object):

    def setup(self):
        self.widget0 = Widget(u'test')
        self.widget1 = Widget(u'nested.test')

    def test_0(self):
        """The root of the validation schema is from `object` type."""
        assert_equal(self.widget0.schema[u'type'], u'object')

    def test_1(self):
        """Convert binding name to property of the root object"""
        assert_in(u'test', self.widget0.schema[u'properties'])

    def test_2(self):
        """
        Binding of nested object is expressed with dot as in javascript and
        is reflected in the schema.
        """
        nested_schema = self.widget1.schema[u'properties'][u'nested']
        assert_in(u'test', nested_schema[u'properties'])

    def test_3(self):
        """
        The leaf object is of the type defined in the as_json property of the
        widget.
        """
        assert_equal(self.widget0.schema[u'properties'][u'test'][u'type'],
                     self.widget0.as_json)

    def test_valid_schema(self):
        """The schema with simple binding is valid."""
        Draft3Validator.check_schema(self.widget0.schema)

    def test_valid_nested_schema(self):
        """The schema with nested binding is valid."""
        Draft3Validator.check_schema(self.widget1.schema)

class TestWidgetValidator(object):

    def setup(self):
        self.val = Validator()
        self.val.attributes = {u'val_attr': u'ok'}
        self.val.alter_schema = mock.Mock(return_value=True)
        self.widget = Widget(u'bind', validators=[self.val])

    def test_alter_schema(self):
        """
        The constructor call the alter_schema method of each validators at
        least once.
        """
        self.val.alter_schema.assert_called_once()
