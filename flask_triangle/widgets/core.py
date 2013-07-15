# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.core
    ---------------------------

    Implements the base widgets of HTML5.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .base import Widget


class Input(Widget):
    """
    Render a basic ``<input>`` field.

    This is the basis for most of the HTML5 widgets.
    """

    html_template = '<input {attributes}/>'
    input_type = None

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None):

        if self.input_type is not None:
            attributes = {'type': self.input_type}
        else:
            attributes = {}
        if html_attributes is not None:
            attributes.update(html_attributes)

        super(Input, self).__init__(bind, name, validators, label,
                                    description, html_attributes)


class TextInput(Input):
    """A simple text input."""
    input_type = 'text'
    json_type = 'text'


class PasswordInput(Input):
    """A password text input."""
    input_type = 'password'
    json_type = 'text'


class EmailInput(Input):
    """An email text input."""
    input_type = 'email'
    json_type = 'text'

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None):

        val = Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-.])*$',
                     client=False)

        if validators is not None:
            validators = [val] + validators
        else:
            validators = [val]

        super(EmailInput, self).__init__(bind, name, validators, label,
                                         description, html_attributes)

class TextArea(Widget):
    """A text input based on the HTML textarea widget."""
    html_template = '<textarea {attributes}></textarea>'
    json_type = 'text'
