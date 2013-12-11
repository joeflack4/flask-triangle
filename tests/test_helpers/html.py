# -*- encoding: utf-8 -*-
"""
    tests.html
    ----------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from nose.tools import assert_true, assert_equal
from nose.plugins.skip import SkipTest

from flask_triangle.helpers import PY3, HTMLString


class TestHtml(object):

    def setup(self):
        self.html = HTMLString('hello')

    def test_0(self):
        """An HTMLString object is of a string type."""
        if PY3:
            assert_true(isinstance(self.html, str))
        else:
            assert_true(isinstance(self.html, unicode))

    def test_1(self):
        """An HTMLString object has a __html__ method."""
        assert_true(hasattr(self.html, '__html__'))

    def test_2(self):
        """The __html__ method returns the string."""
        assert_equal(self.html.__html__(), self.html)
