# -*- encoding: utf-8 -*-
"""
    flask_triangle.form
    -------------------

    Implements the Form class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from .triangle import json_validate
from .widget import Widget
from .types import Schema


class Form(object):
    """
    The Form acts as a container for multiple Widgets.
    """

    __widgets = list()

    @classmethod
    def register_widgets(cls):

        for k, v in cls.__dict__.items():
            if isinstance(v, Widget):
                v.name = k
                if k not in cls.__widgets:
                    cls.__widgets.append(k)

        for parent in cls.__bases__:
            if parent != Form:
                parent.register_widgets()


    def __new__(cls, *args, **kwargs):

        obj = super(Form, cls).__new__(cls)
        cls.register_widgets()

        # Sort all the widgets by their declaration order
        cls.__widgets = sorted(cls.__widgets,
                               key = lambda(k): id(getattr(cls, k)))

        return obj

    def __init__(self, name, schema=None, root=None):
        """
        :arg schema: A ``dict``. A custom schema to describe how-to validate
        resulting JSON from this form.

        :arg root: A ``string``. The name of the properties to use as
        root of the JSON schema.
        """

        if schema is not None:
            self.schema = Schema(schema)
        else:
            self.schema = Schema({})
            for widget in self:
                self.schema.update(widget.schema)

        if root is not None:
            self.schema = self.schema.get('properties').get(root, self.schema)

        self.name = name

    @property
    def validate(self):
        """
        Return a function decorator to validate JSON in the current request.
        """
        return json_validate(self.schema)

    def __iter__(self):
        return (getattr(self, widget) for widget in self.__widgets)
