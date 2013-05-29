# -*- encoding: utf-8 -*-
"""
Test the default behaviour for the common validator.
"""


from flask_triangle.validators.common import Validator
from nose.tools import assert_equal


class TestValidator(object):

    def setup(self):

        self.validator = Validator()

    def test_empty_attributes(self):
        """The default validator does not add an attribute."""
        assert_equal(len(self.validator.attributes()), 0)

    def test_empty_schema(self):
        """The default validator does not alter a schema."""
        assert_equal(len(self.validator.schema()), 0)

