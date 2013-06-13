# -*- encoding: utf-8 -*-
"""
    flask_triangle.widget
    ---------------------

    Implements the Widget class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from flask_triangle.helpers import angular_attribute
from .html import HTMLString
from .schema import Schema


class Widget(object):
    """
    The Widget class is the center component of flask-triangle. Its purpose is
    both to describe the HTML input with a set of client-side validators along
    with creating the JSON-schema for server side validation of transmitted
    data.

    The default Widget is a simple text input.
    """

    html_template = u'<input {attributes}/>'
    as_json = u'string'

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, index=0, **kwargs):

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
        self.index = index

        # applying validator side-effects
        self.attributes = {u'name': name, u'ng-model': bind}
        self._schema = Schema().apply_func(self.init_schema)
        for validator in validators or []:
            self._schema.apply_func(validator.alter_schema)
            self.attributes.update(validator.attributes)

        # update attributes
        for name, value in kwargs.items():
            self.attributes[angular_attribute(name)] = value

    # name is a special attribute also acting as a property.
    @property
    def name(self):
        return self.attributes.get(u'name', None)

    @name.setter
    def name(self, value):
        self.attributes[u'name'] = value

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

    def render_attributes(self):
        """
        Render the attributes as a string with "key=value" chunks, white space
        separated and boolean attributes appearing only as "key".
        """
        def render(k, v):
            """
            Format the key value pair in a string. If the value is suffixed by
            an "|angular" filter, the returned string will be formated to
            render as double curly bracketed in the HTML.
            """
            if v is None:
                return u'{k}'.format(k=k)
            if v.endswith('|angular'):
                return u'{k}="{{{{{{{{{v}}}}}}}}}"'.format(k=k, v=v[:-8])
            return u'{k}="{v}"'.format(k=k, v=v)

        return u' '.join(render(k, v) for k, v in self.attributes.iteritems())

    def init_schema(self, schema, fqn):

        schema.update(Schema({u'type': u'object', u'properties': {}}))

        parent = schema
        for child in self.attributes.get(u'ng-model').split(u'.'):
            new = Schema({u'type': u'object', u'properties': {}})
            parent.get(u'properties')[child] = new
            parent = new

        del parent[u'properties']
        parent[u'type'] = self.as_json

        return True

    def __call__(self, **kwargs):
        """
        Generate the HTML code of the current widget. Keyword arguments are
        used to format the generated HTML.

            >>> a = Widget('hello.world', u'{name}')
            >>> a(name='demo')
            u'<input name="demo" ng-model="hello.world"/>
        """
        if self.name is None:
            raise ValueError(u'The required `name` property is not set.')
        res = self.html_template.format(attributes=self.render_attributes())
        return HTMLString(res.format(**kwargs))
