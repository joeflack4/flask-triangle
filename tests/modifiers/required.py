# -*- encoding: utf-8 -*-
"""
    flask_triangle.tests.modifiers.required
    ---------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from six import text_type
from .dummy import DummyWidget
from flask_triangle.modifiers import Required


class TestRequired(unittest.TestCase):

    def setUp(self):

        self.simple_widget = DummyWidget('simple', modifiers=[Required()])
        self.nested_widget = DummyWidget('nested.property',
                                         modifiers=[Required()])

    def test_simple_schema_is_modified(self):

        self.assertEqual(
            text_type(self.simple_widget.schema),
            '{"properties": {"simple": {"type": "string"}}, "required": ["simpl'
            'e"], "type": "object"}'
        )

    def test_nested_schema_is_modifiers(self):
        self.assertEqual(
            text_type(self.nested_widget.schema),
            '{"properties": {"nested": {"properties": {"property": {"type": "st'
            'ring"}}, "required": ["property"], "type": "object"}}, "required":'
            ' ["nested"], "type": "object"}'
        )
