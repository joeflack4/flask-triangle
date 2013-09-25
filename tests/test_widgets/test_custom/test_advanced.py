# -*- encoding: utf-8 -*-
"""
    tests.widgets.default.custom.advanced
    -------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle import Widget

from jsonschema import Draft3Validator
from nose.tools import raises, assert_true, assert_equal


class AdvancedCustomWidget(Widget):

    html_template = '<tag {{widget.html_attributes}}></tag>'
    schema = {'type': 'string'}

    def __customize__(self):
        self.customize = True


class AdvancedOptionalCustomWidget(Widget):

    html_template = '<tag {{widget.html_attributes}}></tag>'
    schema = {'type': 'string'}

    def __customize__(self, optional='default'):
        self.optional = optional


class AdvancedRequiredCustomWidget(Widget):

    html_template = '<tag {{widget.html_attributes}}></tag>'
    schema = {'type': 'string'}

    def __customize__(self, required):
        self.required = required


class TestCustomizeMethod(object):

    def setup(self):
        self.widget = AdvancedCustomWidget('bind')

    def test_customize(self):
        """
        if it exists a __customize__, this method is called.
        """
        assert_true(self.widget.customize)


class TestOptionalCustomizeMethod(object):
    
    def test_0(self):
        """
        if the __customize__ method expect an optional argument, the argument
        names is salvaged from the kwargs of the widget's constructor
        """
        widget = AdvancedOptionalCustomWidget('bind', optional='test')
        assert_equal(widget.optional, 'test')

    def test_1(self):
        """
        if the __customize__ method expect an optional argument, and the
        argument name cannot be found in the constructor's kwargs, the default
        value is used instead.
        """
        widget = AdvancedOptionalCustomWidget('bind',)
        assert_equal(widget.optional, 'default')


class TestRequiredCustomizeMethod(object):
    
    def test_0(self):
        """
        if the __customize__ method expect an argument, the argument
        names is salvaged from the kwargs of the widget's constructor
        """
        widget = AdvancedRequiredCustomWidget('bind', required='test')
        assert_equal(widget.required, 'test')

    @raises(TypeError)
    def test_1(self):
        """
        if the __customize__ method expect an argument, and the argument name
        cannot be found in the constructor's kwargs and no default value exists,
        a TypeError is raised.
        """
        widget = AdvancedRequiredCustomWidget('bind')
