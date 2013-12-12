# -*- encoding: utf-8 -*-
"""
    tests.forms
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle import Form
from flask_triangle.widgets.standard import TextInput
from nose.tools import assert_equal, assert_in


class TestFormCreation(object):

    def setup(self):
        pass

    def test_form_name(self):
        """A form has a name."""
        form = Form('test')
        assert_equal(form.name, 'test')

    def test_form_default_schema(self):
        """A form has a default schema."""
        form = Form('test')
        assert_equal(form.schema, {})

    def test_custom_schema(self):
        """A form can have a custom schema."""
        form = Form('test', schema={'custom': 'schema'})
        assert_equal(form.schema, {'custom': 'schema'})

# required for test
class MyForm(Form):

    entry1 = TextInput('entry1')
    entry0 = TextInput('entry0')


class TestFormWithWidgets(object):

    def setup(self):
        self.form = MyForm('test')

    def test_widget_direct_access(self):
        """A widget is accessible as an instance property of the object"""
        assert_equal(type(self.form.entry0), TextInput)

    def test_widget_default_name(self):
        """
        A widget without a default name uses the property holding it name as
        its name.
        """
        assert_equal(self.form.entry0.name, 'entry0')

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

