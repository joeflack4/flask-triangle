# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from flask_triangle.validators.common import Validator
from flask_triangle.types import Schema, Attributes


class Regexp(Validator):
    """
    Adds a regular expresion constraint to an input.

    ..note: This validator does not support string format.
    """

    alter_schema = (False, False, True)

    def __init__(self, regexp):
        """
        :arg regexp: A ``regular expression``. The result must match the
        regular expression to be valid.

        See `Angular's input API` for more detail.

        .. _`Angular's input API`:
            http://docs.angularjs.org/api/ng.directive:input
        """
        self.regexp = regexp

    def schema(self, **kwargs):
        return Schema({u'pattern': self.regexp})

    def attributes(self):
        res = self.regexp.replace(u'{', u'{{').replace(u'}', u'}}')
        return Attributes({u'ng-pattern': res})
