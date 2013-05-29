# -*- encoding: utf-8 -*-
"""
Test constructor options of a Widget object.
"""


from flask_triangle.widget import Widget
from nose.tools import assert_equal, assert_not_in, assert_in


class TestFixedArgs(object):

    def setup(self):
        self.widget = Widget(u'bound', u'name', id_='id',
                             custom=u'test', boolean=None)

    def test_bound(self):
        """
        A widget must have a `ng-model` bound value.
        """
        assert_equal(self.widget.attributes.get(u'ng-model'), u'bound')

    def test_id_missing(self):
        """when _id is not set, there is no 'id' key in the attributes."""
        test = Widget(u'bound')
        assert_not_in(u'id', test.attributes)

    def test_id(self):
        """id_ is a special argument to set the id attribute."""
        assert_equal(self.widget.attributes.get(u'id'), u'id')

    def test_class_missing(self):
        """
        when _class is not set, there is no 'class' key in the attributes.
        """
        assert_not_in(u'class', self.widget.attributes)

    def test_class_simple(self):
        """
        when _class is a string, the attributes hold a key/value pair where
        'class' is the key, and the string is the value.
        """
        test = Widget(u'bound', class_=u'class')
        assert_equal(test.attributes.get(u'class'), u'class')

    def test_class_list(self):
        """
        when _class is a list of string, the attributes hold a key/value pair
        where 'class' is the key, and the value is a concatenation, space
        separated, of the string in the list.
        """
        test = Widget(u'bound', class_=[u'class', u'demo'])
        assert_in(u'class', test.attributes.get(u'class'))
        assert_in(u'demo', test.attributes.get(u'class'))
