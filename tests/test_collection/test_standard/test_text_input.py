# -*- encoding: utf-8 -*-
"""
    tests.collection.standard.text_input
    ------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets.standard import (
    TextInput, EmailInput, Textarea,
    PasswordInput, NumberInput
)
from nose.tools import raises, assert_true, assert_in

import re, jsonschema

class CommonTest(object):

    def testValidHTMLRendering(self):
        """
        make a simple rendering check to test if the generated HTML is valid.
        """
        assert_true(re.match('<("[^"]*"|\'[^\']*\'|[^\'">])*>', self.widget()))


    def testExpectedHTML(self):
        """
        check if the HTML structure is the one expected.
        """
        assert_true(re.match('<input (.*?)></input>', self.widget()))


class TestTextInput(CommonTest):

    def setup(self):
        self.widget = TextInput('nested.value')

    def testMinimumAttributeSet(self):
        """
        make a simple rendering check to test if the minimum criterias are met.
        """
        assert_in('type="text"', self.widget())

    def testValidating(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 'valid'}})


class TestPasswordInput(TestTextInput):

    def setup(self):
        self.widget = PasswordInput('nested.value')

    def testMinimumAttributeSet(self):
        """
        make a simple rendering check to test if the minimum criterias are met.
        """
        assert_in('type="password"', self.widget())


class TestEmailInput(CommonTest):

    def setup(self):
        self.widget = EmailInput('nested.value')

    def testMinimumAttributeSet(self):
        """
        make a simple rendering check to test if the minimum criterias are met.
        """
        assert_in('type="email"', self.widget())

    def testValidating(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 'valid@email'}})

    @raises(jsonschema.ValidationError)
    def testFailure(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 'error'}})


class TestNumberInput(CommonTest):

    def setup(self):
        self.widget = NumberInput('nested.value')

    def testMinimumAttributeSet(self):
        """
        make a simple rendering check to test if the minimum criterias are met.
        """
        assert_in('type="number"', self.widget())

    def testValidating(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 0}})

    @raises(jsonschema.ValidationError)
    def testFailure(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 'error'}})


class TestTextarea(CommonTest):

    def setup(self):
        self.widget = Textarea('nested.value')

    def testExpectedHTML(self):
        """
        Override the standard test.
        """
        assert_true(re.match('<textarea (.*?)></textarea>', self.widget()))

    def testValidating(self):
        """
        validate expected data.
        """
        self.widget.schema.validate({'nested': {'value': 'valid'}})
