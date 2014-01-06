# -*- encoding: utf-8 -*-
"""
    test.widget.attributes
    ----------------------

    Is considered as an attribute a property rendered as an HTML attribute
    (i.e. `key="value"` for valued attributes and `key` for boolean attributes)

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget

from nose.tools import assert_equal, assert_not_in, assert_in


class CustomWidget(Widget):
    """
    A custom widget for testing purpose only.
    """
    html_template = '{{attr}}'


class TestAttribute0(object):
    """
    Default object's properties behavior.
    """

    def test_bind(self):
        """
        the bind argument render its value as data-ng-model HTML attribute.
        """
        w = CustomWidget('test')
        assert_equal(w(), 'data-ng-model="test"')

    def test_name0(self):
        """
        the name argument does render in the HTML attribute.
        """
        w = CustomWidget('test', name='test')
        assert_in('name="test"', w())

    def test_name1(self):
        """
        when name is None, the attributes is never rendered.
        """
        w = CustomWidget('test', name='test')
        w.name = None
        assert_not_in('name', w())

    def test_label(self):
        """
        the label arguement does not render in the HTML attribute.
        """
        w = CustomWidget('test', label='test')
        assert_not_in('label', w())

    def test_metadata(self):
        """
        the metadata arguement does not render in the HTML attribute.
        """
        w = CustomWidget('test', metadata='test')
        assert_not_in('metadata', w())

    def test_modifiers(self):
        """
        the modifiers arguement does not render in the HTML attribute.
        """
        w = CustomWidget('test', modifiers=[])
        assert_not_in('modifiers', w())


class TestAttribute1(object):
    """
    Custom attributes management.
    """

    def test_custom_init0(self):
        """
        An attribute set at the construction render as an HTML attribute.
        """
        w = CustomWidget('test', test='success')
        assert_in('test="success"', w())

    def test_custom_init1(self):
        """
        An attribute set at the construction and updated later render as an
        up-to-date HTML attribute.
        """
        w = CustomWidget('test', test='success')
        w.test = 'big success'
        assert_in('test="big success"', w())

    def test_custom_noinit(self):
        """
        An object attribute set after the construction is not rendered as an
        attribute.
        """
        w = CustomWidget('test')
        w.test = 'big success'
        assert_not_in('test="big success"', w())
        assert_equal(w.test, 'big success')
