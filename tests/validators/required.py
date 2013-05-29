# -*- encoding: utf-8 -*-
"""
Test the default behaviour for the Required validator.
"""


from flask_triangle.validators import Required
from nose.tools import assert_equal, assert_in


class TestRequired(object):

    def setup(self):

        self.validator = Required()
        self.condition = Required('0 != 1')

    def test_alter(self):
        """Required alter root and nodes only."""
        assert_equal(self.validator.alter_schema, (True, True, False))

    def test_default_attributes(self):
        """
        By default the required validator add a boolean attributes 'required'.
        """
        assert_in(u'required', self.validator.attributes())
        assert_equal(self.validator.attributes().get(u'required'), None)

    def test_default_schema(self):
        """
        By default the required validator add a property 'required' with a list
        containing the name of the child node.
        """
        assert_in(u'required', self.validator.schema(child=u'child'))
        assert_equal(self.validator.schema(child=u'child').get(u'required'),
                     [u'child'])

    def test_condition_schema(self):
        """
        When an expression is set as condition, the schema is empty.
        """
        assert_equal(len(self.condition.schema()), 0)

    def test_condition_attributes(self):
        """
        When an expression is set as condition; the attributes 'ng-required' is
        set with the expression as the value.
        """
        assert_in(u'ng-required', self.condition.attributes())
        assert_equal(self.condition.attributes().get(u'ng-required'), '0 != 1')

    def test_condition_false(self):
        """
        When the condition is false, the field is not required.
        """
        test = Required(False)
        assert_equal(len(test.attributes()), 0)
