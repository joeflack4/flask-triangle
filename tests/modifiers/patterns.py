# -*- encoding: utf-8 -*-
"""
    flask_triangle.tests.modifiers.patterns
    ---------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from six import text_type
from .dummy import DummyWidget
from flask_triangle.modifiers import Regexp


class TestRegexp(unittest.TestCase):

    def setUp(self):

        self.simple_widget = DummyWidget(
            'simple',
            modifiers=[Regexp('[A-Z0-9]+')]
        )

        self.nested_widget = DummyWidget(
            'nested.property',
            modifiers=[Regexp('[A-Z0-9]+')]
        )

    def test_simple_schema_is_modified(self):
        self.assertEqual(
            text_type(self.simple_widget.schema),
            '{"properties": {"simple": {"pattern": "[A-Z0-9]+", "type": "string'
            '"}}, "type": "object"}'
        )

    def test_nested_schema_is_modifiers(self):
        self.assertEqual(
            text_type(self.nested_widget.schema),
            '{"properties": {"nested": {"properties": {"property": {"pattern": '
            '"[A-Z0-9]+", "type": "string"}}, "type": "object"}}, "type": "obje'
            'ct"}'
        )
