# -*- encoding: utf-8 -*-
"""
Test widget rendering to HTML.
"""


import re

from flask_triangle.widget import Widget
from nose.tools import assert_true, assert_in


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

    def test_rendering_format(self):
        """
        Rendering of widget is formatabale
        """
        test = Widget(u'bound', name=u'name', string_format='{test}')
        assert_in('string_format="ok"', test(test=u'ok'))

    def test_rendering_angular(self):
        """
        Attributes suffixed by `|angular` are angular expressions.
        """
        test = Widget(u'bound', name=u'name', angular='true|angular')
        assert_in('angular="{{true}}"', test())

    def test_rendering_angular_format(self):
        """
        Rendering of widget is formatable inside angular expressions.
        """
        test = Widget(u'bound', name=u'name', angular='{test}|angular')
        assert_in('angular="{{ok}}"', test(test=u'ok'))
