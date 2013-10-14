# -*- encoding: utf-8 -*-
"""
    tests.widgets.collections.uibootstrap.typeahead
    -----------------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle

from flask_triangle.widgets.uibootstrap import Datepicker
from datetime import datetime
import jsonschema

from nose.tools import assert_equal
from tests import cvr


class TestTypeahead(object):

    def setup(self):
        self.app = flask.Flask(__name__)
        triangle = Triangle(self.app)


    def test_0(self):
        """
        no pop-up simple rendering
        """
        simple = Datepicker('bind')
        with self.app.test_request_context():
            assert_equal(cvr(simple()), '<div data-datepicker data-ng-model="bind"></div>')

    def test_1(self):
        """
        pop-up simple rendering
        """
        simple = Datepicker('bind', popup=True)
        with self.app.test_request_context():
            assert_equal(cvr(simple()), '<input data-datepicker-popup="fullDate" data-is-open="_bind" data-ng-click="_bind != _bind;" data-ng-init="_bind = false;" data-ng-model="bind" type="text"></input>')

    def test_2(self):
        """
        controllable pop-up rendering
        """
        simple = Datepicker('bind', popup='control')
        with self.app.test_request_context():
            assert_equal(cvr(simple()), '<input data-datepicker-popup="fullDate" data-is-open="control" data-ng-click="control != control;" data-ng-model="bind" type="text"></input>')

    def test_3(self):
        """
        schema testing
        """
        data = {'bind': datetime.now().isoformat()}
        simple = Datepicker('bind', popup='control')
        jsonschema.validate(data, simple.schema)
