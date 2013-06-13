# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from __future__ import absolute_import
from flask_triangle.validator import Validator


class Regexp(Validator):
    """
    Adds a regular expresion constraint to an input.

    ..note: This validator does not support string format.
    """

    def __init__(self, regexp):
        """
        :arg regexp: A ``regular expression``. The result must match the
        regular expression to be valid.

        See `Angular's input API` for more detail.

        .. _`Angular's input API`:
            http://docs.angularjs.org/api/ng.directive:input
        """
        self.regexp = regexp

    @property
    def attributes(self):
        res = self.regexp.replace(u'{', u'{{').replace(u'}', u'}}')
        return {u'ng-pattern': u'/{}/'.format(res)}

    def alter_schema(self, schema, fqn):
        if schema[u'type'] != 'object':
            schema[u'pattern'] = self.regexp
