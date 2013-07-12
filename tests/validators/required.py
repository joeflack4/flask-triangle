# -*- encoding: utf-8 -*-
"""
    tests.validators.required
    -------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import assert_equal, assert_in, assert_not_in

from flask_triangle.validators import Required
from flask_triangle.schema import Schema


class TestRequired(object):

    def setup(self):
        self.validator_false = Required(False)
        self.validator_default = Required()
        self.validator_conditional = Required('a_value|angular')

    def test_0(self):
        """Add a boolean 'required' attribute"""
        assert_in('required', self.validator_default.attributes)
        assert_equal(self.validator_default.attributes['required'], None)

    def test_1(self):
        """
        Add a 'ng-required' attribute when the required is a client-side
        condition.
        """
        assert_in('ng-required', self.validator_conditional.attributes)
        assert_equal(self.validator_conditional.attributes['ng-required'],
                     'a_value|angular')

    def test_2(self):
        """
        Alter the schema by adding a required field to the schema for each
        named properties.
        """
        schema = Schema({'type': 'object',
                 'properties': {'normal': Schema({'type': 'string'})}})

        schema.apply_func(self.validator_default.alter_schema)

        assert_in('required', schema)
        assert_equal(schema['required'], ['normal'])

    def test_3(self):
        """
        The schema is not altered if the required condition is only client side.
        """
        schema = Schema({'type': 'object',
                 'properties': {'normal': Schema({'type': 'string'})}})

        schema.apply_func(self.validator_conditional.alter_schema)

        assert_not_in('required', schema)

    def test_4(self):
        """
        When the required status is set to False, no attribute is set.
        """
        assert_equal(self.validator_false.attributes, {})
