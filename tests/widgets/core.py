# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets.core import TextInput, EmailInput, PasswordInput
from nose.tools import assert_in


class TestTextInput(object):

    def setup(self):
        self.input = TextInput('test', name='test')

    def test_simple_render(self):
        assert_in('type="text"', self.input())


class TestPasswordInput(object):

    def setup(self):
        self.input = PasswordInput('test', name='test')

    def test_simple_render(self):
        assert_in('type="password"', self.input())


class TestEmailInput(object):

    def setup(self):
        self.input = EmailInput('test', name='test')

    def test_simple_render(self):
        assert_in('type="email"', self.input())
