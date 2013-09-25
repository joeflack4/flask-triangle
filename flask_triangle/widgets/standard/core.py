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

from flask_triangle.widget import Widget
import flask_triangle.modifiers


class Input(Widget):
    """
    HTML input element control with angular data-binding. Input control follows
    HTML5 input types and polyfills the HTML5 validation behavior for older
    browsers.
    """

    schema = {'type': 'string'}

    html_template = '<input {{widget.html_attributes}}></input>'

    def __customize__(self, required=False, min_length=None, max_length=None,
                      pattern=None, change=None):

        if required is not False:
            self.modifiers.append(flask_triangle.modifiers.Required(required))
        if min_length is not None:
            pass    #TODO
        if max_length is not None:
            pass    #TODO
        if pattern is not None:
            self.modifiers.append(flask_triangle.modifiers.Regexp(pattern))
        if change is not None:
            self.html_attributes['data-ng-change'] = change

class TextInput(Input):
    """
    Standard HTML text input with angular data binding.
    """

    def __customize__(self, trim=True):
        self.html_attributes['type'] = 'text'




####################################
'''
class Input(Widget):
    """
    Render a basic ``<input>`` field.

    This is the basis for most of the HTML5 widgets.
    """

    html_template = '<input {attributes}/>'
    input_type = None

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None):

        super(Input, self).__init__(bind, name, validators, label,
                                    description, html_attributes)

        if self.input_type is not None:
            self.attributes.update({'type': self.input_type})


class TextInput(Input):
    """A simple text input."""
    input_type = 'text'
    json_type = 'string'


class PasswordInput(Input):
    """A password text input."""
    input_type = 'password'
    json_type = 'string'


class EmailInput(Input):
    """An email text input."""
    input_type = 'email'
    json_type = 'string'

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


class CheckboxInput(Input):
    """A simple checkbox."""
    input_type = 'checkbox'
    json_type = 'boolean'


class RadioInput(Input):
    """A radio button."""
    input_type = 'radio'
    json_type = 'string'
    html_template = '<input {attributes}>{value}</input>'

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None, value=None):
        super(RadioInput, self).__init__(bind, name, validators, label,
                                         description, html_attributes)
        if value is not None:
            self.attributes['value'], self.value = value
        else:
            self.value = ''

    def render(self):
        if self.name is None:
            raise ValueError('The required `name` property is not set.')
        return self.html_template.format(attributes=unicode(self.attributes),
                                         value=self.value)


class RadioGroupInput(Input):
    """A list of radio buttons."""
    def __init__(self, bind, values, name=None, validators=None, label=None,
                 description=None, html_attributes=None):

        # for compatibility purposes
        super(RadioGroupInput, self).__init__(bind, name, validators, label,
                                              description, html_attributes)

        self.radios = list()
        for k, v in values.iteritems():
            self.radios.append(RadioInput(bind, name, validators, label,
                                          description, html_attributes, (k,v)))

    def render(self):
        return '<br/>'.join(radio.render() for radio in self.radios)


class TextArea(Widget):
    """A text input based on the HTML textarea widget."""
    html_template = '<textarea {attributes}></textarea>'
    json_type = 'string'
'''

