# -*- encoding: utf-8 -*-
"""
    tests.widgets.collections.standard.select
    -----------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle
from flask_triangle.widgets.standard import Select

from nose.tools import assert_equal
from tests import cvr

class TestSelectInput(object):

    def setup(self):
        self.app = flask.Flask(__name__)
        triangle = Triangle(self.app)

    def test_0(self):
        """
        simple angular select
        """
        with self.app.test_request_context():
            select = Select('bind', name='name',
                            options='label for value in array')
            assert_equal(cvr(select()),
                         '<select data-ng-model="bind" data-ng-options="label for value in array" name="name">'
                         '</select>')

    def test_1(self):
        """
        server-side option list with no label and no group
        """
        with self.app.test_request_context():
            select = Select('bind', name='name',
                            options=[('choice0',),
                                     ('choice1',),
                                     ('choice2',),
                                     ('choice3',),
                                     ('choice4',)])
            assert_equal(cvr(select()),
                         '<select data-ng-model="bind" name="name">'
                         '<option>choice0</option>'
                         '<option>choice1</option>'
                         '<option>choice2</option>'
                         '<option>choice3</option>'
                         '<option>choice4</option>'
                         '</select>')

    def test_2(self):
        """
        server-side option list with label and no group
        """
        with self.app.test_request_context():
            select = Select('bind', name='name',
                            options=[('choice0', 'value0'),
                                     ('choice1', 'value1'),
                                     ('choice2', 'value2'),
                                     ('choice3', 'value3'),
                                     ('choice4', 'value4')])
            assert_equal(cvr(select()),
                         '<select data-ng-model="bind" name="name">'
                         '<option value="value0">choice0</option>'
                         '<option value="value1">choice1</option>'
                         '<option value="value2">choice2</option>'
                         '<option value="value3">choice3</option>'
                         '<option value="value4">choice4</option>'
                         '</select>')

    def test_3(self):
        """
        server-side option list with label and no group
        """
        with self.app.test_request_context():
            select = Select('bind', name='name',
                            options=[('choice0', 'value0'),
                                     ('choice1', 'value1', 'group0'),
                                     ('choice2', 'value2', 'group0'),
                                     ('choice3', 'value3', 'group1'),
                                     ('choice4', 'value4', 'group1')])
            assert_equal(cvr(select()),
                         '<select data-ng-model="bind" name="name">'
                         '<option value="value0">choice0</option>'
                         '<optgroup label="group0">'
                         '<option value="value1">choice1</option>'
                         '<option value="value2">choice2</option>'
                         '</optgroup>'
                         '<optgroup label="group1">'
                         '<option value="value3">choice3</option>'
                         '<option value="value4">choice4</option>'
                         '</optgroup>'
                         '</select>')

    def test_4(self):
        """
        Enable multiselect.
        """
        with self.app.test_request_context():
            select = Select('bind', name='name', multiple=True,
                            options='label for value in array')
            assert_equal(cvr(select()),
                         '<select data-ng-model="bind" data-ng-options="label for value in array" multiple name="name">'
                         '</select>')
