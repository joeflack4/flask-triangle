# -*- encoding: utf-8 -*-
"""
    tests.widgets.default.custom.inheritance
    ----------------------------------------

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


class AdvancedOptionalCustomWidget(AdvancedCustomWidget):

    html_template = '<othertag {{widget.html_attributes}}></othertag>'
    schema = {'type': 'string'}

    def __customize__(self, optional='default'):
        self.optional = optional


class AdvancedRequiredCustomWidget(AdvancedOptionalCustomWidget):

    def __customize__(self, required):
        self.optional = required


class AdvancedDuplicateCustomWidget(AdvancedOptionalCustomWidget):

    def __customize__(self, optional):
        self.duplicate = optional


class TestOptionalCustomizeMethod(object):
    
    def test_0(self):
        """
        If the the parent(s) class of a widget has(have) a __customize__ method,
        each __customize__ method of object hierarchy is called once.
        """
        widget = AdvancedOptionalCustomWidget('bind', optional='test')
        assert_equal(widget.optional, 'test')
        assert_true(widget.customize)

    def test_1(self):
        """
        Optional argument behavior of __customize__ is maintained.
        """
        widget = AdvancedOptionalCustomWidget('bind')
        assert_equal(widget.optional, 'default')
        assert_true(widget.customize)

    @raises(TypeError)
    def test_2(self):
        """
        Required argument behavior of __customize__ is maintained.
        """
        widget = AdvancedRequiredCustomWidget('bind')

    def test_3(self):
        """
        If the same argument name is used in multiple __customize__ method,
        the same argument from the constructor's kwargs is used.
        """
        widget = AdvancedDuplicateCustomWidget('bind', optional='test')
        assert_equal(widget.optional, 'test')
        assert_equal(widget.duplicate, 'test')

    @raises(TypeError)
    def test_4(self):
        """
        The required behavior override the optional one when the same
        argument is used in different __customize__ method using both of them.
        """
        widget = AdvancedDuplicateCustomWidget('bind')

    def test_5(self):
        """
        The __customize__ methods of classes are called in the inheritance
        order.
        """
        widget = AdvancedRequiredCustomWidget('bind', optional='old',
                                              required='new')
        assert_equal(widget.optional, 'new')
