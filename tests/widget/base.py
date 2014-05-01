# -*- encoding: utf-8 -*-
"""
    flask-triangle.tests.widgets.base
    ---------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle.widgets.widget import Widget
import unittest


class TestBaseWidget(unittest.TestCase):


    def test_label_not_set(self):
        """
        if not set, label property returns the value of the name property
        """

        widget = Widget('binding', name='name')
        self.assertEqual(widget.label, widget.name)
        self.assertEqual(widget.label, 'name')

    def test_label_set(self):

        widget = Widget('binding', name='name', label='label')
        self.assertNotEqual(widget.label, widget.name)
        self.assertEqual(widget.label, 'label')

    def test_label_reset(self):

        widget = Widget('binding', name='name')
        self.assertEqual(widget.label, widget.name)
        widget.label = 'label'
        self.assertNotEqual(widget.label, widget.name)
        self.assertEqual(widget.label, 'label')

    def test_name_reset(self):
        widget = Widget('binding', name='name')
        self.assertEqual(widget.label, widget.name)
        widget.name = 'renamed'
        self.assertEqual(widget.label, widget.name)
