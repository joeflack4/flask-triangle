# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.core
    ---------------------------

    Implement the base widgets of HTML5 supported by AngularJS.

    * input

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets import Widget
from flask_triangle.schema import String, Number
from flask_triangle.schema.format import Email


class Input(Widget):
    """
    The default input widget.
    """
    schema = String()
    html_template = '<input {{attr}}></input>'


class TextInput(Input):
    """
    """

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'text'
        super(TextInput, self).__init__(bind, name, label, modifiers, metadata,
                                        **kwargs)


class Textarea(Input):
    """
    HTML textarea element control with angular data-binding.
    """
    html_template = '<textarea {{attr}}></textarea>'


class PasswordInput(Input):
    """
    """

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'password'
        super(PasswordInput, self).__init__(bind, name, label, modifiers, metadata,
                                            **kwargs)


class EmailInput(Input):
    """
    """

    schema = Email()

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'email'
        super(EmailInput, self).__init__(bind, name, label, modifiers, metadata,
                                         **kwargs)


class NumberInput(Input):
    """
    """

    schema = Number()

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):

        kwargs['type'] = 'number'
        super(NumberInput, self).__init__(bind, name, label, modifiers, metadata,
                                          **kwargs)