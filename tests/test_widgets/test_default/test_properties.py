# -*- encoding: utf-8 -*-
"""
    tests.widgets.default.properties
    --------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle import Widget
from nose.tools import raises, assert_equal, assert_not_in, assert_is, \
                       assert_true


class TestBindProperty(object):

    def setup(self):
        self.widget = Widget('test0')

    @raises(TypeError)
    def test_0(self):
        """
        __init__ requires `bind` argument to be set.
        """
        Widget()

    def test_1(self):
        """
        bind is readable through the `bind` property.
        """
        assert_equal(self.widget.bind, 'test0')

    def test_2(self):
        """
        bind is writable through the `bind` property.
        """
        self.widget.bind = 'test1'
        assert_equal(self.widget.bind, 'test1')

    def test_3(self):
        """
        bind is tightened to the `data-ng-model` HTML attribute.
        """
        assert_equal(self.widget.html_attributes['data-ng-model'],
                     self.widget.bind)

    def test_4(self):
        assert_equal(self.widget.html_attributes['data-ng-model'],
                     self.widget.bind)
        self.widget.bind = 'test1'
        assert_equal(self.widget.html_attributes['data-ng-model'],
                     self.widget.bind)


class TestNameProperty(object):

    def setup(self):
        self.widget = Widget('bind', name='test0')

    def test_0(self):
        """
        the widget's name can be set by the `__init__`
        """
        assert_equal(self.widget.name, 'test0')

    def test_1(self):
        """
        The widget's name can be set by the `name` property
        """
        self.widget.name = 'test1'
        assert_equal(self.widget.name, 'test1')


    def test_2(self):
        """
        `name` is tightened to the `name` HTML attribute.
        """
        assert_equal(self.widget.html_attributes['name'],
                     self.widget.name)

    def test_3(self):
        assert_equal(self.widget.html_attributes['name'],
                     self.widget.name)
        self.widget.name = 'test1'
        assert_equal(self.widget.html_attributes['name'],
                     self.widget.name)

    def test_4(self):
        """
        if name is set to None, the name attribute is deleted from the HTML
        attributes.
        """
        assert_equal(self.widget.html_attributes['name'],
                     self.widget.name)
        self.widget.name = None
        assert_not_in('name', self.widget.html_attributes)

    def test_5(self):
        """
        if name is None, name returns None
        """
        self.widget.name = None
        assert_is(self.widget.name, None)


class TestLabelProperty(object):

    def setup(self):
        self.widget = Widget('bind', name='name', label='test0')

    def test_0(self):
        """
        the widget's label can be set by the `__init__`
        """
        assert_equal(self.widget.label, 'test0')

    def test_1(self):
        """
        The widget's label can be set by the `label` property
        """
        self.widget.label = 'test1'
        assert_equal(self.widget.label, 'test1')

    def test_2(self):
        """
        if label is not set, the label return the name value
        """
        self.widget.label = None
        assert_equal(self.widget.label, self.widget.name)


class TestOtherProperties(object):

    def setup(self):
        self.widget = Widget('bind')

    def test_0(self):
        """
        the widget has a schema property
        """
        assert_true(hasattr(self.widget, 'schema'))

    def test_1(self):
        """
        the widget has a description property
        """
        assert_true(hasattr(self.widget, 'description'))

    def test_2(self):
        """
        the widget has a list of modifiers which is empty by default
        """
        assert_equal(self.widget.modifiers, [])
