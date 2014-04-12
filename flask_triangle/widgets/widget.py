# -*- encoding: utf-8 -*-
"""
    flask_triangle.widget
    ---------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jinja2

from flask_triangle.schema import Schema
from flask_triangle.helpers import HTMLString, HTMLAttrs


class Widget(object):
    """
    """

    # the instance counter is used to keep track of the widget order in a form.
    instance_counter = 0

    # the default HTML template
    html_template = (
        '<em>'
        'This widget is not renderable.'
        '</em>'
    )

    # the atomic_schema
    atomic_schema = None

    @property
    def bind(self):
        return self.html_attributes.get('ngModel', None)

    @bind.setter
    def bind(self, value):
        self.html_attributes['ngModel'] = value

    @property
    def name(self):
        return self.html_attributes.get('name', None)

    @bind.setter
    def name(self, value):
        self.html_attributes['name'] = value

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
        self._schema.compile()
        return self._schema

    def __init__(self, bind, name=None, label=None, description=None,
                 html_attributes=None, modifiers=None):

        # increment the instance counter
        self.instance_counter = Widget.instance_counter
        Widget.instance_counter += 1

        self.html_attributes = HtmlAttrs()
        self._schema = Schema()
        self.modifiers = []             # TODO: handle this

        # default properties
        self.bind = bind                # is an HTML attribute (see properties)
        self.name = name                # is an HTML attribute (see properties)
        self.label = label
        self.description = description

        self.init_schema()
        self.apply_modifiers()

        # set the optional attributes
        if html_attributes is not None:
            self.html_attributes(html_attributes)

    def init_schema(self):
        """
        Initialize the schema.
        """

        def fqn_to_schema(schema, fqn):
            schema.update(Schema({'type': 'object', 'properties': {}}))

            # Convert the fully qualified name of the widget (dotted notation) to
            # nested subschemas. See it as a tree with one branch
            parent = schema
            for child in self.bind.split('.')[:-1]:
                new = Schema({'type': 'object', 'properties': {}})
                parent['properties'][child] = new
                parent = new

            # Finally the atomic schema is the leaf of this one-branch tree
            last = self.bind.split('.')[-1]
            parent['properties'][last] = Schema(self.__class__.atomic_schema)
            return True

        self._schema.apply_func(fqn_to_schema)

    def apply_modifiers(self):
        """
        Update the schema and the HTML attributes in regards of the modifiers.
        """
        for modifier in self.modifiers:

            if hasattr(modifier, 'alter_schema'):
                self.schema.apply_func(modifier.alter_schema)

            if hasattr(modifier, 'attributes'):
                self.html_attributes.update(modifier.attributes)

    def __unicode__(self):

        return jinja2.Template(self.html_template).render(widget=self)

    def __str__(self):
        # Python2/3 compatibility
        if sys.version_info > (3, 0):
            return self.__unicode__()
        return unicode(self).encode('utf-8')
