# -*- encoding: utf-8 -*-
"""
Test the handling of inputs in a form
"""


from flask_triangle.widgets import TextInput
from flask_triangle import Form

from nose.tools import assert_equal, assert_in


class MyForm(Form):

    entry1 = TextInput(u'entry1')
    entry0 = TextInput(u'entry0')


class TestWidgetManagement(object):

    def setup(self):

        self.myform = MyForm(u'my_form')

    def test_direct_access(self):
        """A widget is accessible as any other field"""
        assert_equal(type(self.myform.entry0), TextInput)

    def test_input_init(self):
        """
        The name of a widget is automatically set to the property name held
        it in the Form object.
        """
        assert_equal(self.myform.entry0.name, u'entry0')

    def test_iterate_init(self):
        """
        Iterating other a Form instance allows to access each held Widgets
        in the order of their declaration
        """

        widget_list = [widget.name for widget in self.myform]
        assert_equal(len(widget_list), 2)
        assert_in('entry0', widget_list)
        assert_in('entry1', widget_list)

class TestSchemaManagement(object):

    def setup(self):

        self.auto = MyForm(u'my_form')
        self.manual = MyForm(u'my_form', {})

    def test_schema_auto(self):
        """
        By default, the schema by merging every schemas of held widgets.
        """
        schema = self.auto.schema

        assert_in(u'entry1', schema['properties'])
        assert_in(u'entry0', schema['properties'])

    def test_schema_manual(self):
        """
        A custom schema can be set
        """
        assert_equal(len(self.manual.schema), 0)
