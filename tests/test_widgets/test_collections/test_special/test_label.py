# -*- encoding: utf-8 -*-
"""
    tests.widgets.collections.special.label
    ---------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle

from flask_triangle.widgets.special import Label

from nose.tools import assert_equal
from tests import cvr


class TestLabel(object):

    def setup(self):
        self.app = flask.Flask(__name__)
        triangle = Triangle(self.app)

        self.simple = Label('bind', name='name')

    def test_0(self):
        """
        simple rendering
        """
        with self.app.test_request_context():
            assert_equal(cvr(self.simple()), '<input name="name" value="{{bind}}">')

