# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets.core import TextInput, EmailInput, PasswordInput,\
                                        CheckboxInput, RadioInput,\
                                        RadioGroupInput
from nose.tools import assert_in, assert_equal


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


class TestCheckboxInput(object):

    def setup(self):
        self.input = CheckboxInput('test', name='test')

    def test_simple_render(self):
        assert_in('type="checkbox"', self.input())


class TestRadioInput(object):

    def test_simple_render0(self):
        widget = RadioInput('test', name='test')
        assert_in('type="radio"', widget())

    def test_simple_render1(self):
        widget = RadioInput('test', name='test', value=('attribute', 'details'))
        assert_in('value="attribute"', widget())
        assert_in('>details<', widget())


class TestRadioGroupInput(object):

    def setup(self):
        self.widget = RadioGroupInput('test', name='test',
                                      values={'attribute0': 'details0',
                                              'attribute1': 'details1'})

    def test_render_one(self):
        """
        rendering a radio group with one attribute is equal as rendering a
        a radio input.
        """
        widget = RadioGroupInput('test', name='test',
                                 values={'attribute': 'details'})
        assert_equal(widget(), RadioInput('test', name='test',
                                          value=('attribute', 'details'))())

    def test_render_multiple0(self):
        """
        rendering multiple radio in a radio group are separated with <br/>.
        """
        assert_in('<br/>', self.widget())

    def test_render_multiple1(self):
        """
        each input in a radio group are equivalent to a radio.
        """
        atoms = self.widget().split('<br/>')
        for atom in atoms:
           if 'details0' in atom:
                assert_equal(atom,
                             RadioInput('test', name='test',
                                        value=('attribute0', 'details0'))())

           if 'details1' in atom:
                assert_equal(atom,
                             RadioInput('test', name='test',
                                        value=('attribute1', 'details1'))())
