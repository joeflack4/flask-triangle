# -*- encoding: utf-8 -*-
"""
    test.forms.inheritance
    ----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle import Form
from flask_triangle.widgets.standard import TextInput

from nose.tools import assert_equal


class Original(Form):

    entry1 = TextInput('entry1')
    entry0 = TextInput('entry0')


class Inherited(Original):

    entry2 = TextInput('entry2')


class Overloaded(Original):

    entry2 = TextInput('entry2')
    entry1 = TextInput('overloaded_entry1')


class TestInheritance0(object):

    def setup(self):

        self.original = Original('original')

    def test_no_side_effects(self):
        """An child class does not modify its parent class."""
        assert_equal(len([widget for widget in self.original]), 2)
        assert_equal(self.original.entry1.name, 'entry1')


class TestInheritance1(object):

    def setup(self):

        self.inherited = Inherited('inherited')

    def test_parent_widgets_remains_in_child_class(self):
        """A child class keeps its parent widgets."""
        assert_equal(self.inherited.entry0.name, 'entry0')
        assert_equal(self.inherited.entry1.name, 'entry1')

    def test_new_widget_are_present_in_child_class(self):
        """A child class has its own widgets."""
        assert_equal(self.inherited.entry2.name, 'entry2')

    def test_iterate_order(self):
        """The iteration order put widget parents before."""
        assert_equal([widget.name for widget in self.inherited],
                     ['entry1', 'entry0', 'entry2'])


class TestInheritance2(object):

    def setup(self):
        self.overloaded = Overloaded('overloaded')

    def test_overloaded_property_is_not_parent_property(self):
        """
        A widget overloaded in the child is not the same as in the parent.
        """
        assert_equal(self.overloaded.entry1.bind, 'overloaded_entry1')

    def test_original_overloaded_property_are_dropped(self):
        """
        A widget overloaded in the child does not duplicate when iterating over
        the latter.
        """
        assert_equal(len([widget for widget in self.overloaded]), 3)

    def test_original_order_is_preserved(self):
        """
        The iterating order is preserved when a widget is overloaded.
        """
        assert_equal([widget.name for widget in self.overloaded],
                     ['entry1', 'entry0', 'entry2'])
