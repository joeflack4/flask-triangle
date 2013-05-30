# -*- encoding: utf-8 -*-
"""
Test the default behaviour for the Required validator.
"""


from flask_triangle.validators import Regexp
from nose.tools import assert_equal, assert_in


class TestRegexp(object):

    def setup(self):

        self.validator = Regexp(u'[A-Z]{3}')

    def test_alter(self):
        """Regexp alters leaf only."""
        assert_equal(self.validator.alter_schema, (False, False, True))

    def test_attributes(self):
        """
        The regexp validator add an attribute 'ng-pattern'. Curly-brackets are
        escaped.
        """
        assert_in(u'ng-pattern', self.validator.attributes())
        assert_equal(self.validator.attributes().get(u'ng-pattern'), 
                     u'[A-Z]{{3}}')

    def test_schema(self):
        """
        The schema to be merged with the lead contains a 'pattern' property
        with the validating regular expression as value.
        """
        assert_in(u'pattern', self.validator.schema())
        assert_equal(self.validator.schema().get(u'pattern'), u'[A-Z]{3}')
