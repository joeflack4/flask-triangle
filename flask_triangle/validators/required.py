# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from flask_triangle.validators.common import Validator
from flask_triangle.types import Schema, Attributes


class Required(Validator):
    """
    Adds a required constraint to an input.

    A required input will sets ``required`` validation error key if the value
    is not entered on the client-side. The associated mapping will be set as
    required in the JSON-schema on the server-side.

    If the requirement of the field is dynamic (i.e. defined from the client
    side by an ``angular expression``), the server-side JSON-schema will
    consider this field as optional.
    """

    alter_schema = (True, True, False)

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

    def schema(self, **kwargs):
        if self.condition is True:
            return Schema({u'required': [u'{child}'.format(**kwargs)]})
        return Schema()

    def attributes(self):
        if self.condition is True:
            return Attributes({u'required': None})
        if self.condition:
            return Attributes({u'ng-required': self.condition})
        return Attributes()
