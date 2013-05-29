# -*- encoding: utf-8 -*-
"""
Test widget rendering to HTML.
"""


import re

from flask_triangle.widget import Widget
from nose.tools import assert_true


class TestRendering(object):

    def setup(self):
        self.widget = Widget(u'bound', name=u'name')

    def test_rendering_on_call(self):
        """
        When calling a widget instance it returns a string.
        """
        assert_true(issubclass(self.widget().__class__, unicode))

    def test_rendering_is_html(self):
        """
        Rendering of a widget is valid HTML.
        """
        assert_true(re.match(r'<("[^"]*"|\'[^\']*\'|[^\'">])*>',
                    self.widget()))
