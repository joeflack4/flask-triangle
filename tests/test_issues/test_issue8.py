# -*- encoding: utf-8 -*-
"""
    Issue #8
    --------

    https://github.com/morgan-del/flask-triangle/issues/8

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle import Form
from flask_triangle.widgets.standard import TextInput, Textarea
from flask_triangle.widgets.special import Label

from nose.tools import assert_equal, assert_in



class NewApplicationForm(Form):
    """
    Create a new application form.
    """

    title = TextInput('application.title', name='title',
                      required=True)

    applicant = TextInput('application.applicant', name='applicant',
                          required=True)

    description = Textarea('application.description', name='description',
                           required=True)


class EditApplicationForm(NewApplicationForm):
    """
    Edit a new application form.
    Editing an application doesn't let you change the title and the applicant.
    """

    title = Label('application.title')
    applicant = Label('application.applicant')


class TestIssue8(object):

    def setup(self):
        self.new_application = NewApplicationForm('issue8', root="application")
        self.edit_application = EditApplicationForm('issue8', root="application")

    def test_valid_schema(self):
        assert_in('description', self.edit_application.schema['required'])
        assert_equal(len(self.edit_application.schema['required']), 1)
