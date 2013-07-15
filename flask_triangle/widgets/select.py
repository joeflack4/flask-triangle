# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from .base import Widget


class SelectInput(Widget):
    """A Select input."""

    html_template = '<select {attributes}>{options}</select>'
    json_type = 'string'

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None, choices=None):
        """
        :arg choices: a list of tuple or a string. The string is an angular
        generator expression. Otherwise, each tuple can be from one to three
        element long. The first one is the displayed value in the select,
        the second the effective value of the element if different from the
        displayed value (or None), the last element is a containing group.
        """

        super(SelectInput, self).__init__(bind, name, validators, label,
                                          description, html_attributes)

        self.choices = None
        if isinstance(choices, list):
            self.choices = choices
        else:
            self.attributes['ng-options'] = choices

    def render_options(self):
        res = ''
        if self.choices is not None:
            choices = sorted([option + (None, None)[0:3-len(option)]
                              for option in self.choices], key=lambda x: x[2])

            current_group = None
            for title, value, group in choices:
                if group != current_group:
                    if current_group is not None:
                        res += '</optgroup>'
                    res += '<optgroup label="{}">'.format(group)
                    current_group = group

                if value is not None:
                    res += '<option value="{}">{}</option>'.format(value, title)
                else:
                    res += '<option>{}</option>'.format(title)
            if current_group is not None:
                res += '</optgroup>'
        return res

    def render(self):
        if self.name is None:
            raise ValueError('The required `name` property is not set.')
        return self.html_template.format(attributes=unicode(self.attributes),
                                         options=self.render_options())
