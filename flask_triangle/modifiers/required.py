# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from __future__ import absolute_import
from .modifier import Modifier
from flask_triangle.schema import Object


class Required(Modifier):
    """
    Adds a required constraint to an input.

    A required input will sets ``required`` validation error key if the value
    is not entered on the client-side. The associated mapping will be set as
    required in the JSON-schema on the server-side.

    If the requirement of the field is dynamic (i.e. defined from the client
    side by an ``angular expression``), the server-side JSON-schema will
    consider this field as optional.
    """

    def __init__(self, condition=True):
        """
        :arg condition: An ``angular expression`` or a boolean value. If
        condition is `True`, the validated input will be required, otherwise,
        if the condition is an angular expression, it will be set as value of
        the ``ng-required`` attribute.

        See `Angular's input API` for more detail.

        .. _`Angular's input API`:
            http://docs.angularjs.org/api/ng.directive:input
        """
        self.condition = condition
        if self.condition is True:
            self.attributes = {u'required': None}
        elif self.condition:
            self.attributes = {u'data-ng-required': self.condition}
        else:
            self.attributes = {}

    def alter_schema(self, schema, bind):

        if self.condition is not True:
            return

        segments = bind.split('.')
        counter = 0
        for fqn, subschema in schema:
            if (fqn is None or bind.startswith(fqn)) and issubclass(type(subschema), Object):
                subschema.required.append(segments[counter])
                counter += 1