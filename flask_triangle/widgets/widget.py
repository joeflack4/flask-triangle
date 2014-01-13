# -*- encoding: utf-8 -*-
"""
    flask_triangle.widget
    ---------------------

    Implements the basic mechanisms of every widgets.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jinja2
from flask_triangle.helpers import HTMLString, camel_to_dash, make_attr
from flask_triangle.schema import Schema, Object


class Widget(object):
    """
    The cornerstone of Flask-Triangle, the class
    :class:`~flask.triangle.widgets.base.Widget` is the base class of every
    widgets.
    """

    schema = None
    html_template = None

    _html_attributes = None     # this must be initialized

    # a counter to keep track of the instantiation order
    _instance_counter = 0

    @property
    def bind(self):
        return self._html_attributes['data-ng-model']

    @bind.setter
    def bind(self, value):
        self._html_attributes['data-ng-model'] = value

    @property
    def label(self):
        if self._label is None:
            return self.name
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def _attr(self):
        """
        Generate the HTML attribute strings of the current widget.
        """
        return ' '.join([make_attr(*i) for i in 
                         sorted(self._html_attributes.items())])

    def __init__(self, bind, name=None, label=None, modifiers=None,
                 metadata=None, **kwargs):
        """
        :arg bind: An assignable ``angular expression`` to data-bind to.
        See ngModel_ directive for more information.
        :arg name: An optional string.
        :arg label: An optional string.
        :arg modifiers: An optional `list` of `Modifiers`. The modifiers are the
        transformations of the widget behavior that impact the value of the
        widget.
        :arg metadata: Additional metadata for the widget. Metadatas aren't
        rendered in the HTML.
        :arg **kwargs: Additional HTML attributes for the widget.

        .. _ngModel: http://docs.angularjs.org/api/ng.directive:ngModel
        """

        # increment the instance counter
        self._instance_counter = Widget._instance_counter
        Widget._instance_counter += 1

        # Initialize the runtime object's properties
        for key in kwargs.keys():
            if camel_to_dash(key) in ['data-ng-model', 'ng-model']:
                raise AttributeError('`ng-model` is automatically generated '
                                     'from the `bind` argument.')

        # the dict is required by later assignation (bind especially)
        self._html_attributes = dict(kwargs)

        self.bind = bind
        self.name = name
        self.metadata = metadata

        self._label = label # see the property for the behavior of the label

        # Create the local schema
        self.schema = Schema()
        if name is not None and name:
            self.schema.title = name

        if self.__class__.schema is not None:
            target = self.schema
            for level in bind.split('.')[:-1]:
                target.properties.add(level, Object())
                target = target.properties[level]

            target.properties.add(bind.rsplit('.', 1)[-1],
                                  self.__class__.schema)

        # Modify the default behaviour
        self.modifiers = []
        if modifiers is not None:
            self.modifiers += modifiers


    def __getattr__(self, name):

        # name and id have custom managment
        if name in ['name', 'id']:
            self._html_attributes.get(name, None)

        if name not in self._html_attributes:
            raise AttributeError
        return self._html_attributes[name]

    def __setattr__(self, name, value):

        # name and id have custom management
        if name in ['name', 'id']:
            if value is None:
                self._html_attributes.pop(name, None)
            else:
                self._html_attributes[name] = value

        if self._html_attributes is not None and name in self._html_attributes:
            self._html_attributes[name] = value
        else:
            super(Widget, self).__setattr__(name, value)

    def __call__(self, **kwargs):
        """
        Generate the HTML code of the current widget. Keyword arguments are
        used to format the generated HTML.

            >>> a = DemoWidget('hello.world', '{name}')
            >>> a(name='demo')
            '<input name="demo" ng-model="hello.world"/>
        """

        # generate the HTML code of the widget
        template = ''
        if self.html_template is not None:
            template = jinja2.Template(self.html_template)\
                             .render(attr=self._attr(), widget=self)

        # return it for rendering
        return HTMLString(template.strip().format(**kwargs))
