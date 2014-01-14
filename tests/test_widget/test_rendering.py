# -*- encoding: utf-8 -*-
"""
    test.widget.rendering
    ---------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget

from nose.tools import assert_equal, assert_not_in, assert_in


class CustomWidget0(Widget):
    """
    A custom widget.
    """
    html_template = '<input {{attr}}>Valid HTML</input>'

class CustomWidget1(Widget):
    """
    A custom widget.
    """
    html_template = '<input {{attr}}>{{widget.property}}</input>'



class Test0(object):

    def test_simple_0(self):
        """
        """
        w = CustomWidget0('test')
        assert_equal(w(), '<input data-ng-model="test">Valid HTML</input>')

    def test_simple_1(self):
        """
        """
        w = CustomWidget0('test', other='big success')
        assert_equal(w(), '<input data-ng-model="test" other="big success">Valid HTML</input>')

    def test_angular(self):
        """
        a value suffixed by |angular render as a double-bracketed Angular JS expression.
        """
        w = CustomWidget0('test', other='var|angular')
        assert_equal(w(), '<input data-ng-model="test" other="{{var}}">Valid HTML</input>')

    def test_parameterized(self):
        """
        a value can be parameterized.
        """
        w = CustomWidget0('test', other='{var}')
        assert_equal(w(var='ok'), '<input data-ng-model="test" other="ok">Valid HTML</input>')

    def test_parameterized_angular(self):
        """
        combination of the precedent tests.
        """
        w = CustomWidget0('test', other='{var}|angular')
        assert_equal(w(var='ok'), '<input data-ng-model="test" other="{{ok}}">Valid HTML</input>')

class Test1(object):

    def test_simple_0(self):
        """
        """
        w = CustomWidget1('test')
        assert_equal(w(), '<input data-ng-model="test"></input>')

    def test_property(self):
        """
        A not-attribute property is resolved in the template.
        """
        w = CustomWidget1('test')
        w.property = 'ok'
        assert_equal(w(), '<input data-ng-model="test">ok</input>')

    def test_parameterized_property(self):
        """
        A not-attribute property is parameterized.
        """
        w = CustomWidget1('test')
        w.property = '{var}'
        assert_equal(w(var='ok'), '<input data-ng-model="test">ok</input>')

    def test_no_angular_property(self):
        """
        the suffix angular is not resolved for not-attribute properties.
        """
        w = CustomWidget1('test')
        w.property = 'ok|angular'
        assert_equal(w(), '<input data-ng-model="test">ok|angular</input>')

    def test_interference(self):
        """
        if a property is also an html attribute, it will appears twice.
        TODO: enhance this behaviour.
        """
        w = CustomWidget1('test', property='ok')
        assert_equal(w(), '<input data-ng-model="test" property="ok">ok</input>')
