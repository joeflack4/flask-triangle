# -*- encoding: utf-8 -*-
"""
    tests.widgets.collections.standard.text
    ---------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle

from flask_triangle.widgets.standard import Textarea
from tests import cvr

from nose.tools import assert_equal


class TestTextarea(object):

    def setup(self):
        self.app = flask.Flask(__name__)
        triangle = Triangle(self.app)

        self.simple = Textarea('bind', name='name')

    def test_0(self):
        """
        simple rendering
        """
        with self.app.test_request_context():
            assert_equal(cvr(self.simple()),
                         '<textarea data-ng-model="bind" name="name">'
                         '</textarea>')

    def test_1(self):
        """
        Modification of the widget's properties are reflected in the rendering.
        """
        with self.app.test_request_context():
            self.simple.bind = 'other'
            assert_equal(cvr(self.simple()),
                         '<textarea data-ng-model="other" name="name">'
                         '</textarea>')

    def test_2(self):
        """
        Parameterized rendering is available.
        """
        with self.app.test_request_context():
            self.simple.bind = '{param}'
            assert_equal(cvr(self.simple(param='ok')),
                         '<textarea data-ng-model="ok" name="name">'
                         '</textarea>')

    def test_3(self):
        """
        Custom TextInput arguments are processed and rendered : simple required
        """
        with self.app.test_request_context():
            required = Textarea('bind', name='name', required=True)
            assert_equal(cvr(required()),
                         '<textarea data-ng-model="bind" name="name" required>'
                         '</textarea>')

    def test_4(self):
        """
        Custom TextInput arguments are processed and rendered : conditional required
        """
        with self.app.test_request_context():
            required = Textarea('bind', name='name', required='angular')
            assert_equal(cvr(required()),
                         '<textarea data-ng-model="bind" data-ng-required="angular" name="name">'
                         '</textarea>')

    def test_5(self):
        """
        Custom TextInput arguments are processed and rendered : pattern
        """
        with self.app.test_request_context():
            pattern = Textarea('bind', name='name', pattern='[A-Z]{5}')
            assert_equal(cvr(pattern()),
                         '<textarea data-ng-model="bind" data-ng-pattern="/[A-Z]{5}/" name="name">'
                         '</textarea>')

    def test_6(self):
        """
        Custom HTML attribute are rendered
        """
        with self.app.test_request_context():
            attr = Textarea('bind', name='name',
                             html_attributes={'data-test': 'test'})
            assert_equal(cvr(attr()),
                         '<textarea data-ng-model="bind" data-test="test" name="name">'
                         '</textarea>')

    def test_7(self):
        """
        Custom HTML attribute can host simple angular expression
        """
        with self.app.test_request_context():
            attr = Textarea('bind', name='name',
                             html_attributes={'data-test': 'test|angular'})
            assert_equal(cvr(attr()),
                         '<textarea data-ng-model="bind" data-test="{{test}}" name="name">'
                         '</textarea>')

    def test_8(self):
        """
        Custom HTML attribute can host complex angular expression
        """
        with self.app.test_request_context():
            attr = Textarea('bind', name='name',
                             html_attributes={'placeholder': 'function(a.nested.param, other)|angular'})
            assert_equal(cvr(attr()),
                         '<textarea data-ng-model="bind" name="name" placeholder="{{function(a.nested.param, other)}}">'
                         '</textarea>')

    def test_9(self):
        """
        Custom HTML attribute can be parameterized.
        """
        with self.app.test_request_context():
            attr = Textarea('bind', name='name',
                             html_attributes={'data-test': '{param}|angular'})
            assert_equal(cvr(attr(param='test')),
                         '<textarea data-ng-model="bind" data-test="{{test}}" name="name">'
                         '</textarea>')

    def test_10(self):
        """
        Custom HTML attribute can host complex parameterized angular expression
        """

        with self.app.test_request_context():
            attr = Textarea('bind', name='name',
                             html_attributes={'placeholder': 'function(a.nested.{param0}, {param1})|angular'})
            assert_equal(cvr(attr(param0='test', param1='success')),
                         '<textarea data-ng-model="bind" name="name" placeholder="{{function(a.nested.test, success)}}">'
                         '</textarea>')

    def test_11(self):
        """
        Custom TextInput arguments are processed and rendered : pattern
        """
        with self.app.test_request_context():
            pattern = Textarea('bind', name='name', min_length='3')
            assert_equal(cvr(pattern()),
                         '<textarea data-ng-minlength="3" data-ng-model="bind" name="name">'
                         '</textarea>')

    def test_12(self):
        """
        Custom TextInput arguments are processed and rendered : pattern
        """
        with self.app.test_request_context():
            pattern = Textarea('bind', name='name', max_length='10')
            assert_equal(cvr(pattern()),
                         '<textarea data-ng-maxlength="10" data-ng-model="bind" name="name">'
                         '</textarea>')
