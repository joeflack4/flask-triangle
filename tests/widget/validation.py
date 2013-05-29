# -*- encoding: utf-8 -*-
"""
Test constructor options of a Widget object.
"""


from flask_triangle.widget import Widget
from flask_triangle.validators import Required
from nose.tools import assert_equal, assert_in


class TestDeclaration(object):

    def test_no_validators(self):

        test = Widget(u'bound')
        assert_equal(len(test.validators), 1)

    def test_validators(self):

        test = Widget(u'bound', validators=[Required()])
        assert_equal(len(test.validators), 2)
        assert_in(Required, (type(validator) for validator in test.validators))
