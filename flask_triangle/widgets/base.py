# -*- encoding: utf-8 -*-
"""
    flask_triangle.widgets.base
    ---------------------------

    Base components and features of every widgets.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import re
from flask_triangle.helpers import UnicodeMixin, HTMLString
from flask_triangle.schema import Schema


class HtmlAttr(dict, UnicodeMixin):
    """
    Implements an object to manage and render attributes of an HTML element.

    HtmlAttr is a dict with a custom rendering method to string. It converts
    camelcase inputs to dash separated notation and removes the value of all
    boolean attributes.

        >>> demo = HtmlAttr(attr='value', boolean=None, camelCase=True)
        >>> print demo
        attr="value" boolean camel-case="true"
    """

    @staticmethod
    def _get_name(string):
        """
        Convert a string to a valid HTML attribute name.
        """
        if re.match(r'^[A-Za-z0-9]+$', string):
            words = re.split(r'(^[a-z]*)|([A-Z][^A-Z]+)', string)
            return '-'.join(c for c in words if c is not None and c).lower()
        return string.lower()

    @staticmethod
    def _get_value(value):
        """
        A value is converted to its string representation. For compatibility
        purpose with Javascript, `True` and `False` are in lower case.
        """
        if type(value) is bool:
            return '"{}"'.format(unicode(value).lower())
        return '"{}"'.format(unicode(value))

    @staticmethod
    def _to_attr(key, value):
        """
        Convert a key value pair to an attribute representation. If value is
        None, the attribute is considered as a boolean attribute present but
        with no value.

        :arg key: A string. The attribute name.
        :arg value: Anything. The value of the attribute.
        :return: A string.
        """
        # anticipated return (no need to process the value)
        if value is None:
            return HtmlAttr._get_name(key)

        return '{name}={value}'.format(name=HtmlAttr._get_name(key),
                                         value=HtmlAttr._get_value(value))

    def __unicode__(self):
        """
        Return all the attributes of a string.
        """
        unique = dict((self._get_name(k), v) for k, v in self.iteritems())
        return ' '.join(self._to_attr(k, v) for k, v in sorted(unique.items()))


class Widget(object):
    """
    The Widget class is the center component of flask-triangle. Its purpose is
    both to describe the HTML input with a set of client-side validators along
    with creating the JSON-schema for server side validation of transmitted
    data.
    """

    instance_counter = 0

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, html_attributes=None):

        """
        :arg bind: An ``angular expression``. Two-way Angular's data binding
        using ngModel directive. See `Angular's ngModel directive` for more
        detail.

        .. _`Angular's ngModel directive`:
            http://docs.angularjs.org/api/ng.directive:ngModel

        :arg name: An ``unicode`` string. The name of the current widget in the
        generated HTML. This argument is optional but the property must be set
        in order to generate the HTML.

        :arg validators: A ``list`` of ``Validator`` instances.

        :arg label: A ``unicode`` string or an ``angular expression``. An
        optional label for the current widget.

        :arg description: A ``unicode`` string or an ``angular expression``. An
        optional description for current widget.

        :arg kwargs: Each keyword arguments will be considered as attributes
        of the HTML rendered widget. The argument starting with "ng[A-Z].*"
        will be converted from camelCase to a dashed version of them to comply
        with the Angular's API. See `Angular's API` for more detail.

        .. _`Angular's API`:
            http://docs.angularjs.org/api/
        """

        self._label = label
        self.description = description

        self.instance_counter = Widget.instance_counter
        Widget.instance_counter += 1

        # applying validator side-effects
        self.attributes = HtmlAttr({'name': name, 'ng-model': bind})
        self._schema = Schema().apply_func(self.init_schema)
        self.validators = validators or []

        for validator in self.validators:
            self._schema.apply_func(validator.alter_schema)
            self.attributes.update(validator.attributes)

        if html_attributes is not None:
            self.attributes.update(html_attributes)

    @property
    def name(self):
        return self.attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def bind(self):
        return self.attributes.get('ng-model', None)

    @bind.setter
    def bind(self, value):
        self.attributes['ng-model'] = value

    @property
    def label(self):
        if self._label is None:
            return self.name
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def schema(self):
        return self._schema.compile()

    def init_schema(self, schema, fqn):

        schema.update(Schema({'type': 'object', 'properties': {}}))

        parent = schema
        for child in self.attributes.get('ng-model').split('.'):
            new = Schema({'type': 'object', 'properties': {}})
            parent.get('properties')[child] = new
            parent = new

        del parent['properties']
        parent['type'] = self.json_type

        return True

    def render(self):
        if self.name is None:
            raise ValueError('The required `name` property is not set.')
        return self.html_template.format(attributes=unicode(self.attributes))

    def __call__(self, **kwargs):
        """
        Generate the HTML code of the current widget. Keyword arguments are
        used to format the generated HTML.

            >>> a = Widget('hello.world', '{name}')
            >>> a(name='demo')
            '<input name="demo" ng-model="hello.world"/>
        """
        return HTMLString(self.render().format(**kwargs))
