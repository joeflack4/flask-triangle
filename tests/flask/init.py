# -*- encoding: utf-8 -*-
"""
    tests.flask.init
    ----------------

    Test the initialization process of the Triangle extension.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle

class TestInit(object):

    def test_init(self):
        """A simple init. Nothing more, nothing less"""

        app = flask.Flask(__name__)
        triangle = Triangle(app)
