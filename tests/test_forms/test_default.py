# -*- encoding: utf-8 -*-
"""
    tests.forms.default
    -------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle import Form
from flask_triangle.schema import Schema
from flask_triangle.widgets.standard import TextInput
from nose.tools import assert_equal, assert_in


class TestEmptyForm(object):
    """
    A serie of tests on the empty form behavior.
    """

    def test_form_name0(self):
        """A form has a name."""
        form = Form('test')
        assert_equal(form.name, 'test')

    def test_form_name1(self):
        """The form name is the title of the schema."""
        form = Form('test')
        assert_equal(form.schema.title, 'test')

    def test_form_default_schema(self):
        """A form has a default schema."""
        form = Form('test')
        assert_equal(form.schema, Schema(title='test',
                                         additional_properties=False))

    def test_custom_schema(self):
        """A form can have a custom schema."""
        form = Form('test', Schema())
        assert_equal(form.schema, Schema())


class MyForm(Form):
    """
    A custom form for testing purpose.
    """
    entry1 = TextInput('entry1')
    entry0 = TextInput('entry0')


class TestFormWithWidgets(object):

    def setup(self):
        self.form = MyForm('test')

    def test_widget_direct_access(self):
        """A widget is accessible as an instance property of the object"""
        assert_equal(type(self.form.entry0), TextInput)
        assert_equal(type(self.form.entry1), TextInput)

    def test_widget_default_name(self):
        """
        A widget without a default name uses the property holding it name as
        its name.
        """
        a = self.form.entry0.name
        assert_equal(self.form.entry0.name, 'entry0')
        assert_equal(self.form.entry1.name, 'entry1')

    def test_iterate(self):
        """
        Iterating other a Form instance allows to access each held Widgets.
        """

        widget_list = [widget.name for widget in self.form]
        assert_equal(len(widget_list), 2)
        assert_in('entry0', widget_list)
        assert_in('entry1', widget_list)

    def test_iterate_order(self):
        """
        When iterating other held widgets, the declaration order is preserved.
        """
        assert_equal([widget.name for widget in self.form],
                     ['entry1', 'entry0'])
