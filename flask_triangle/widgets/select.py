# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from .base import Widget


class SelectInput(Widget):
    """A Select input."""

    html_template = u'<select {attributes}>{options}</select>'
    as_json = u'string'

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
            self.attributes[u'ng-options'] = choices

    def render_options(self):
        """

        """
        res = u''
        if self.choices is not None:

            choices = sorted([option + (None, None)[0:3-len(option)]
                              for option in self.choices], key=lambda x: x[2])

            current_group = None
            for title, value, group in choices:
                if group != current_group:
                    if current_group is not None:
                        res += u'</optgroup>'
                    res += u'<optgroup label="{}">'.format(group)
                    current_group = group

                if value is not None:
                    res += u'<option value="{}">{}</option>'.format(value, title)
                else:
                    res += u'<option>{}</option>'.format(title)
            if current_group is not None:
                res += u'</optgroup>'

        return res


    def render(self):
        if self.name is None:
            raise ValueError(u'The required `name` property is not set.')
        return self.html_template.format(attributes=self.render_attributes(),
                                         options=self.render_options())
