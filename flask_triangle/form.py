# -*- encoding: utf-8 -*-
"""
    flask_triangle.form
    -------------------

    Implements the Form class.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

import six
import copy

from .helpers import json_validate
from .widget import Widget
from .schema import Schema


class FormBase(type):
    """Metaclass for a Form object"""

    def __new__(mcs, name, bases, attrs):

        super_new = super(FormBase, mcs).__new__

        if name == 'NewBase' and attrs == {}:
            return super_new(mcs, name, bases, attrs)
        parents = [b for b in bases if isinstance(b, FormBase) and
                   not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_new(mcs, name, bases, {'__module__': module})

        # widget class attributes are moved in fields
        new_class._Form__widgets = list() if new_class._Form__widgets is None\
                                   else copy.deepcopy(new_class._Form__widgets)

        for obj_name, obj in attrs.items():
            if isinstance(obj, Widget):
                if obj.name is None:
                    obj.name = obj_name
                new_class._Form__widgets.append(obj)
            setattr(new_class, obj_name, obj)

        new_class._Form__widgets.sort(key=lambda k: k.index)
        return new_class


class Form(six.with_metaclass(FormBase)):
    """
    The Form acts as a container for multiple Widgets.
    """

    __widgets = None

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
            self.schema = Schema()
            for widget in self:
                self.schema.merge(widget.schema)
        self.schema.compile()

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
        return (widget for widget in self.__widgets)
