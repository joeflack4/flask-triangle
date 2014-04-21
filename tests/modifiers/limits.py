# -*- encoding: utf-8 -*-
"""
    flask_triangle.tests.modifiers.limits
    -------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from six import text_type
from .dummy import DummyWidget
from flask_triangle.modifiers import LengthLimit


class TestLengthLimitsMin(unittest.TestCase):

    def setUp(self):

        self.simple_widget = DummyWidget(
            'simple',
            modifiers=[LengthLimit(minimum=1)]
        )

        self.nested_widget = DummyWidget(
            'nested.property',
            modifiers=[LengthLimit(minimum=1)]
        )

    def test_simple_schema_is_modified(self):
        self.assertEqual(
            text_type(self.simple_widget.schema),
            '{"properties": {"simple": {"minLength": 1, "type": "string"}}, "ty'
            'pe": "object"}'
        )

    def test_nested_schema_is_modified(self):
        self.assertEqual(
            text_type(self.nested_widget.schema),
            '{"properties": {"nested": {"properties": {"property": {"minLength"'
            ': 1, "type": "string"}}, "type": "object"}}, "type": "object"}'
        )

class TestLengthLimitsMax(unittest.TestCase):

    def setUp(self):

        self.simple_widget = DummyWidget(
            'simple',
            modifiers=[LengthLimit(maximum=1)]
        )

        self.nested_widget = DummyWidget(
            'nested.property',
            modifiers=[LengthLimit(maximum=1)]
        )

    def test_simple_schema_is_modified(self):
        self.assertEqual(
            text_type(self.simple_widget.schema),
            '{"properties": {"simple": {"maxLength": 1, "type": "string"}}, "ty'
            'pe": "object"}'
        )

    def test_nested_schema_is_modified(self):
        self.assertEqual(
            text_type(self.nested_widget.schema),
            '{"properties": {"nested": {"properties": {"property": {"maxLength"'
            ': 1, "type": "string"}}, "type": "object"}}, "type": "object"}'
        )
