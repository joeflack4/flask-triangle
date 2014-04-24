# -*- encoding: utf-8 -*-
"""
    flask-triangle.tests.widgets.customize
    --------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from flask_triangle.widgets.widget import Widget


class DummyWidget0(Widget):

    def customize(self, optional_arg=True):
        self.customized = True
        self.optional_arg = optional_arg


class DummyWidget1(Widget):

    def customize(self, required_arg):
        self.required_arg = required_arg


class DummyWidget2(DummyWidget0):

    def customize(self, another_arg=False):
        self.double_customized = True
        self.another_arg = another_arg


class DummyWidget3(Widget):

    def customize(self, attribute=None):
        self.html_attributes['attribute'] = attribute


class TestCustomize(unittest.TestCase):

    def test_customize_call(self):

        widget = DummyWidget0('bind')
        self.assertEqual(widget.customized, True)

    def test_customize_greed_init_kwargs(self):

        widget = DummyWidget0('bind', optional_arg='ok')
        self.assertEqual(widget.optional_arg, 'ok')

    def test_customize_raise_error_required_arg(self):

        with self.assertRaises(TypeError):
            widget = DummyWidget1('bind')

    def test_customize_succeed(self):

        widget = DummyWidget1('bind', required_arg='ok')
        self.assertEqual(widget.required_arg, 'ok')


class TestCustomizeInheritance(unittest.TestCase):

    def test_customize_all_call(self):

        widget = DummyWidget2('bind')
        self.assertEqual(widget.double_customized, True)
        self.assertEqual(widget.customized, True)

    def test_customize_greed_init_kwargs(self):

        widget = DummyWidget2('bind', optional_arg='ok')
        self.assertEqual(widget.optional_arg, 'ok')

    def test_customize_greed_init_kwargs(self):

        widget = DummyWidget2('bind', another_arg='ok')
        self.assertEqual(widget.another_arg, 'ok')


class TestCustomizePriority(unittest.TestCase):

    def test_user_override_inheritance(self):

        widget = DummyWidget3(
            'bind',
            attribute='fail',
            html_attributes={'attribute': 'ok'}
        )
        self.assertEqual(widget.html_attributes['attribute'], 'ok')
