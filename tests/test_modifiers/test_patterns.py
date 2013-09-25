# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import assert_equal, assert_in, assert_not_in

from flask_triangle.modifiers import Regexp, PatternProperty
from flask_triangle.schema import Schema


class TestRegexp(object):

    def setup(self):
        self.validator = Regexp('[A-Z]{4}')

    def test_0(self):
        """Create a dict with an ng-pattern value."""
        assert_in('ng-pattern', self.validator.attributes)

    def test_1(self):
        """
        Attribute value is prefixed and suffixed by slashes to conform with the
        javascript regexp notation.
        """
        assert_equal(self.validator.attributes['ng-pattern'][0],
                     '/')
        assert_equal(self.validator.attributes['ng-pattern'][-1],
                     '/')

    def test_2(self):
        """Curly bracket are escaped in the regexp."""
        assert_equal(self.validator.attributes['ng-pattern'], '/[A-Z]{{4}}/')

    def test_3(self):
        """
        Insert a pattern to the leaf objects.
        If a schema is altered by the validator, only the leafs ared affected
        by the modifications.
        """
        schema = Schema({'type': 'object',
                         'properties': {'normal': Schema({'type': 'string'})},
                         'required': ['normal']})

        schema.apply_func(self.validator.alter_schema)

        assert_in('pattern', schema['properties']['normal'])

    def test_4(self):
        """
        The value of the pattern in the schema is not modified.
        If a schema is altered by the validator, only the leafs ared affected
        by the modifications.
        """
        schema = Schema({'type': 'object',
                 'properties': {'normal': Schema({'type': 'string'})},
                 'required': ['normal']})

        schema.apply_func(self.validator.alter_schema)

        assert_in('[A-Z]{4}', schema['properties']['normal']['pattern'])


class TestPatternProperty(object):
    """
    Tests are done with a schema having a variable with 'parent.child' as FQN;
    """

    def setup(self):
        self.schema = Schema({'type': 'object',
                              'properties': {'parent': Schema({'type': 'object',
                                                                 'properties': {'child': Schema({'type': 'string'})}})}})

    def test_0(self):
        """PatternProperty does not set attributes."""
        assert_equal(PatternProperty().attributes, {})

    def test_1(self):
        """
        The FQN redefinition can be partial and will not raise an exception.
        """
        validator = PatternProperty(r'^[A-Z]{3}')
        self.schema.apply_func(validator.alter_schema)

    def test_2(self):
        """
        The FQN redefinition add an asPatternProperty field to the object if
        the argument does not match the FQN.
        """
        validator = PatternProperty(r'^[A-Z]{3}')
        self.schema.apply_func(validator.alter_schema)
        assert_in('asPatternProperty', self.schema['properties']['parent'])

    def test_3(self):
        """
        The FQN redefinition set the asPatternProperty field value to the value
        of the argument if it does not match the FQN.
        """
        validator = PatternProperty(r'^[A-Z]{3}')
        self.schema.apply_func(validator.alter_schema)
        assert_equal(self.schema['properties']['parent']['asPatternProperty'],
                     r'^[A-Z]{3}')

    def test_4(self):
        """
        If the FQN is not redefined, no modification is done.
        """
        validator = PatternProperty('parent')
        self.schema.apply_func(validator.alter_schema)
        assert_not_in('asPatternProperty',
                      self.schema['properties']['parent'])

