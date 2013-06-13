# -*- encoding: utf-8 -*-
"""
    tests.helpers
    -------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from flask_triangle.helpers import angular_attribute, angular_filter
from nose.tools import assert_equal


class TestHelperAngularAttribute(object):

    def test_angular_attribute0(self):
        """attributes which aren't angular styled are not modified"""
        assert_equal(angular_attribute(u'test'), u'test')

    def test_angular_attribute1(self):
        """angular attributes are converted from camelcase to dashed style."""
        assert_equal(angular_attribute(u'ngTest'), u'ng-test')

    def test_angular_attribute2(self):
        """
        angular attributes are converted from camelcase to dashed style and
        capitalized acronyms are preserved as distinct words.
        """
        assert_equal(angular_attribute(u'ngTestHTML'), u'ng-test-html')


    def test_angular_attribute3(self):
        """
        angular attributes are converted from camelcase to dashed style and
        capitalized acronyms are preserved as distinct words.
        """
        assert_equal(angular_attribute(u'ngHTML'), u'ng-html')


    def test_angular_attribute4(self):
        """
        angular attributes are converted from camelcase to dashed style and
        capitalized acronyms are preserved as distinct words.
        """
        assert_equal(angular_attribute(u'ngHTMLTest'), u'ng-html-test')


    def test_angular_attribute5(self):
        """
        Possible bug
        """
        assert_equal(angular_attribute(u'ngTngTest'), u'ng-tng-test')

    def test_angular_attribute6(self):
        """
        Possible bug
        """
        assert_equal(angular_attribute(u'ngTngtoto'), u'ng-tngtoto')


class TestHelperJnijaAngularFilter(object):
    
    def test_filter(self):
        """Test the jinja2 filter"""
        assert_equal(angular_filter(u'test'), u'{{test}}')


