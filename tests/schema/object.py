# -*- encoding: utf-8 -*-
"""
    test.schema
    -----------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from six import text_type
from flask_triangle.schema import Object, String

import unittest


class TestObjectProperties(unittest.TestCase):

    def test_required(self):

        obj = Object(required=['ok'])
        self.assertEqual(
            text_type(obj),
            '{"properties": {}, "required": ["ok"], "type": "object"}'
        )

    def test_maxproperties(self):

        obj = Object(max_properties=5)
        self.assertEqual(
            text_type(obj),
            '{"maxProperties": 5, "properties": {}, "type": "object"}'
        )

    def test_minproperties(self):

        obj = Object(min_properties=5)
        self.assertEqual(
            text_type(obj),
            '{"minProperties": 5, "properties": {}, "type": "object"}'
        )

    def test_additionalproperties(self):

        obj = Object(additional_properties=False)
        self.assertEqual(
            text_type(obj),
            '{"additionalProperties": false, "properties": {}, "type": "object"}'
        )


class TestObjectFeatures(unittest.TestCase):

    def setUp(self):

        self.obj = Object()
        self.ref = String()

    def test_add_property(self):

        self.obj['test'] = self.ref
        self.assertIs(self.obj['test'], self.ref)

    def test_add_deep_property(self):

        self.obj['this.is.a.test'] = self.ref
        self.assertIs(self.obj['this.is.a.test'], self.ref)
        self.assertIs(self.obj['this']['is']['a']['test'], self.ref)

    def test_contains(self):

        self.obj['this.is.a.test'] = self.ref
        self.assertIn('this', self.obj)
        self.assertIn('this.is', self.obj)
        self.assertIn('this.is.a', self.obj)
        self.assertIn('this.is.a.test', self.obj)

    def test_schema_simple(self):

        self.obj['test'] = self.ref
        self.assertEqual(
            text_type(self.obj),
            '{"properties": {"test": {"type": "string"}}, "type": "object"}'
        )

    def test_schema_deep(self):

        self.obj['this.is.a.test'] = self.ref
        self.assertEqual(
            text_type(self.obj),
            '{"properties": {"this": {"properties": {"is": {"properties": {"a":'
            ' {"properties": {"test": {"type": "string"}}, "type": "object"}}, '
            '"type": "object"}}, "type": "object"}}, "type": "object"}'
        )

    def test_missing_key0(self):

        with self.assertRaises(KeyError):
            self.obj['missing']

    def test_missing_key1(self):

        self.obj['this.is.a.test'] = self.ref

        with self.assertRaises(KeyError):
            self.obj['this.is.missing']

    def test_iter(self):

        self.obj['this.is.a.test'] = self.ref

        for k, v in self.obj:
            if k is not None:
                self.assertIs(self.obj[k], v)
            else:
                self.assertIs(self.obj, v)
