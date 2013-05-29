# -*- encoding: utf-8 -*-
"""
Test basic properties of a Widget object.
"""


from flask_triangle.widget import Widget
from nose.tools import assert_equal, assert_in


class TestWidgetProperties(object):

    def test_name_0(self):
        """
        name is a property.
        """

        test = Widget(u'bind')
        test.name = u'name'

        assert_equal(test.name, u'name')

    def test_name_1(self):
        """
        name is an attribute.
        """

        test = Widget(u'bind')
        test.name = u'name'

        assert_in(u'name', test.attributes)
        assert_equal(u'name', test.attributes.get(u'name'))

    def test_label_0(self):
        """
        label is a property.
        """

        test = Widget(u'bind', name=u'name')
        test.label = u'label'

        assert_equal(test.label, u'label')

    def test_label_1(self):
        """
        label returns the name value if not set.
        """

        test = Widget(u'bind', name=u'name')
        assert_equal(test.label, u'name')
