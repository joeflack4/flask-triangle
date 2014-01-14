# -*- encoding: utf-8 -*-
"""
    test.widget.properties
    ----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget

from nose.tools import assert_equal, assert_true, raises


class TestWidgetProperties(object):
    """
    Test the properties of a widget.
    """

    def test_any_properties(self):
        """
        Any keyword argument of a Widget become a property of it.
        """
        w = Widget('test', testProperty='ok')
        assert_true(hasattr(w, 'testProperty'))
        assert_equal(w.testProperty, 'ok')

    @raises(AttributeError)
    def test_missing_property(self):
        """
        Trying to access an unitialized property raises the expected 
        AttributeError.
        """
        w = Widget('test')
        w.missingProperty

    def test_label0(self):
        """
        If not set, label returns the name value.
        """
        w = Widget('test', name='name')
        assert_equal(w.label, w.name)

    def test_label1(self):
        """
        If set, label returns its own value.
        """
        w = Widget('test', name='name', label='label')
        assert_equal(w.label, 'label')

    def test_label2(self):
        """
        Changing name does not modify label.
        """
        w = Widget('test', name='name', label='label')
        w.name = 'new_name'
        assert_equal(w.label, 'label')

    @raises(AttributeError)
    def test_reserved_kwargs0(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', dataNgModel='ko')

    @raises(AttributeError)
    def test_reserved_kwargs1(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', DataNgModel='ko')

    @raises(AttributeError)
    def test_reserved_kwargs2(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', **{'data-ng-model': 'ko'})

    @raises(AttributeError)
    def test_reserved_kwargs3(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', ngModel='ko')

    @raises(AttributeError)
    def test_reserved_kwargs4(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', NgModel='ko')

    @raises(AttributeError)
    def test_reserved_kwargs5(self):
        """
        defining a data-ng-model, ng-model or any derivated argument should
        raise an attribute error AttributeError.
        """
        Widget('test', **{'ng-model': 'ko'})
