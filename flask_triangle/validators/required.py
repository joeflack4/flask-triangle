# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from flask_triangle.validator import Validator


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

        super(Required, self).__init__()
        if condition is True:
            self.attributes[u'required'] = None
        elif condition:
            self.attributes[u'ng-required'] = condition

    def is_required(self):
        """
        Returns `True` if the field is inconditionally required, `False`
        otherwise.
        """

        return 'required' in self.attributes
