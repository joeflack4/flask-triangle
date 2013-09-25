# -*- encoding: utf-8 -*-
"""
    tests.widgets.default.rendering
    -------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle import Widget
from nose.tools import assert_equal

class TestBindProperty(object):

    def setup(self):
        self.widget = Widget('test0', name='demo')

    def test_0(self):
        """
        The standard widget render a default error message.
        """
        assert_equal(self.widget(), '<em>This Flask-Triangle widget is not renderable.</em>')
