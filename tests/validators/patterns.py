# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from nose.tools import assert_equal, assert_in, assert_not_in

from flask_triangle.validators import Regexp, PatternProperty
from flask_triangle.schema import Schema

class TestRegexp(object):

    def setup(self):
        self.validator = Regexp('[A-Z]{4}')

    def test_0(self):
        """Create a dict with an ng-pattern value."""
        assert_in(u'ng-pattern', self.validator.attributes)

    def test_1(self):
        """
        Attribute value is prefixed and suffixed by slashes to conform with the
        javascript regexp notation.
        """
        assert_equal(self.validator.attributes[u'ng-pattern'][0], 
                     u'/')
        assert_equal(self.validator.attributes[u'ng-pattern'][-1], 
                     u'/')

    def test_2(self):
        """Curly bracket are escaped in the regexp."""
        assert_equal(self.validator.attributes[u'ng-pattern'], u'/[A-Z]{{4}}/')

    def test_3(self):
        """
        Insert a pattern to the leaf objects.
        If a schema is altered by the validator, only the leafs ared affected
        by the modifications.
        """
        schema = Schema({u'type': u'object',
                         u'properties': {u'normal': Schema({u'type': u'string'})},
                         u'required': [u'normal']})

        schema.apply_func(self.validator.alter_schema)

        assert_in(u'pattern', schema[u'properties'][u'normal'])

    def test_4(self):
        """
        The value of the pattern in the schema is not modified.
        If a schema is altered by the validator, only the leafs ared affected
        by the modifications.
        """
        schema = Schema({u'type': u'object',
                 u'properties': {u'normal': Schema({u'type': u'string'})},
                 u'required': [u'normal']})

        schema.apply_func(self.validator.alter_schema)

        assert_in(u'[A-Z]{4}', schema[u'properties'][u'normal'][u'pattern'])


class TestPatternProperty(object):
    """
    Tests are done with a schema having a variable with 'parent.child' as FQN;
    """

    def setup(self):
        self.schema = Schema({u'type': u'object',
                              u'properties': {u'parent': Schema({u'type': u'object',
                                                                 u'properties': {u'child': Schema({u'type': u'string'})}})}})

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
        assert_in(u'asPatternProperty', self.schema[u'properties'][u'parent'])

    def test_3(self):
        """
        The FQN redefinition set the asPatternProperty field value to the value
        of the argument if it does not match the FQN.
        """
        validator = PatternProperty(r'^[A-Z]{3}')
        self.schema.apply_func(validator.alter_schema)
        assert_equal(self.schema[u'properties'][u'parent'][u'asPatternProperty'],
                     r'^[A-Z]{3}')

    def test_4(self):
        """
        If the FQN is not redefined, no modification is done.
        """
        validator = PatternProperty(u'parent')
        self.schema.apply_func(validator.alter_schema)
        assert_not_in(u'asPatternProperty',
                      self.schema[u'properties'][u'parent'])

