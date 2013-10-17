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
from flask_triangle.widgets.standard import TextInput
from flask_triangle.widgets.special import Label
from flask_triangle.modifiers import Regexp

from nose.tools import assert_not_in


class NewItem(Form):

    description = TextInput('item.description', required=True)
    code = TextInput('item.code', modifiers=[Regexp(r'^$|^[A-Z0-9]*$')])

class EditItem(NewItem):

    code = Label('item.code')


class TestIssue8(object):

    def setup(self):
        self.new = NewItem('issue9', root="item")
        self.edit = EditItem('issue9', root="item")

    def test_valid_schema(self):
        assert_not_in('code', self.edit.schema['properties'])
