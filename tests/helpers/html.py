# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

from six import text_type
from flask_triangle.helpers import HTMLAttrs


class HTMLAttrsTest(unittest.TestCase):

    def setUp(self):

        self.attr = HTMLAttrs()

        self.attr['attribute'] = 'ok'
        self.attr['boolean'] = None
        self.attr['camelCase'] = 'too'
        self.attr['dash-syntax'] = 'yeah'

    def test_simple_attr(self):

        self.assertIn('attribute', self.attr)
        self.assertEqual(self.attr['attribute'], 'ok')

    def test_conversion_0(self):

        self.assertIn('camel-case', self.attr)
        self.assertIn('camelCase', self.attr)
        self.assertEqual(self.attr['camel-case'], 'too')
        self.assertEqual(self.attr['camelCase'], 'too')

    def test_conversion_1(self):

        self.assertIn('dash-syntax', self.attr)
        self.assertIn('dashSyntax', self.attr)
        self.assertEqual(self.attr['dash-syntax'], 'yeah')
        self.assertEqual(self.attr['dashSyntax'], 'yeah')

    def test_remove_attr_0(self):

        del self.attr['attribute']
        self.assertNotIn('attribute', self.attr)

    def test_remove_attr_1(self):

        del self.attr['camelCase']
        self.assertNotIn('camel-case', self.attr)
        self.assertNotIn('camelCase', self.attr)

    def test_remove_attr_2(self):

        del self.attr['camel-case']
        self.assertNotIn('camel-case', self.attr)
        self.assertNotIn('camelCase', self.attr)

    def test_exception_0(self):

        with self.assertRaises(KeyError):
            self.attr['missing']

    def test_exception_1(self):

        with self.assertRaises(KeyError):
            del self.attr['missing']

    def test_iter(self):

        for k in self.attr:
            self.assertIn(
                k, ['attribute', 'boolean', 'camel-case', 'dash-syntax']
            )

    def test_items(self):

        res = {
            'attribute': 'ok',
            'boolean': None,
            'camel-case': 'too',
            'dash-syntax': 'yeah',
        }

        for k, v in self.attr.items():
            self.assertIn(
                k, ['attribute', 'boolean', 'camel-case', 'dash-syntax']
            )
            self.assertEqual(v, res[k])

    def test_alternate_init(self):

        attr = HTMLAttrs(attribute='ok', boolean=None, camelCase='too')

        self.assertIn('boolean', attr)
        self.assertEqual(attr['boolean'], None)
        self.assertIn('attribute', attr)
        self.assertEqual(attr['attribute'], 'ok')
        self.assertIn('camel-case', attr)
        self.assertIn('camelCase', attr)
        self.assertEqual(attr['camel-case'], 'too')
        self.assertEqual(attr['camelCase'], 'too')

class HTMLAttrsRenderingTest(unittest.TestCase):


    def test_rendering(self):

        attr = HTMLAttrs()
        attr['attribute'] = 'ok'
        attr['boolean'] = None
        attr['camelCase'] = 'too'
        attr['dash-syntax'] = 'yeah'

        self.assertEqual(
            text_type(attr),
            'attribute="ok" boolean camel-case="too" dash-syntax="yeah"'
        )

    def test_boolean(self):
        """
        Boolean value are rendered in lowercase.
        """

        attr = HTMLAttrs(firstValue=True, secondValue=False)
        self.assertIn('second-value="false"', text_type(attr))
        self.assertIn('first-value="true"', text_type(attr))

    def test_angular_suffic(self):
        """
        When |angular suffix is used, angular's variable notation is used.
        """

        attr = HTMLAttrs(key="variable|angular")
        self.assertEqual('key="{{variable}}"', text_type(attr))
