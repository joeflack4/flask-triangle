# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask_triangle import Triangle
from flask_triangle import Form
from flask_triangle.widgets.core import TextInput
from nose.tools import assert_in


t = flask.render_template_string


class SimpleForm(Form):

    entry1 = TextInput('entry1')
    entry0 = TextInput('entry0')


class FormatForm(Form):

    entry1 = TextInput('entry1', name='{replace}')
    entry0 = TextInput('entry0')


class TestRender(object):

    def setup(self):
        self.app = flask.Flask(__name__)
        triangle = Triangle(self.app)

    def test_simple_rendering(self):
        """
        Test if rendering raises any error.
        """
        with self.app.test_request_context():
            t('{{test()}}', test=SimpleForm('my_form'))


    def test_rendering_and_replace(self):
        """
        Test if rendering formats string.
        """
        with self.app.test_request_context():
            res = t('{{test(replace=\'ok\')}}', test=FormatForm('my_form'))
            assert_in('name="ok"', res)
