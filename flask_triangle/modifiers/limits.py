# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.limits
    -------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


class Minimum(Modifier):
    """
    Add a minimum value validation.
    """

    def __init__(self, value):
        """
        """
        self.value
    
    @property
    def attributes(self):
        return {'min': value}

    def alter_schema(self, schema, fqn):
        if schema['type'] != 'object':
            schema['minimum'] = self.value


class Maximum(Modifier):
    """
    Add a maximum value validation.
    """

    def __init__(self, value):
        """
        """
        self.value
    
    @property
    def attributes(self):
        return {'max': value}

    def alter_schema(self, schema, fqn):
        if schema['type'] != 'object':
            schema['maximum'] = self.value


class MinimumLength(Modifier):
    """
    Add a minimum value validation.
    """

    def __init__(self, value):
        """
        """
        self.value
    
    @property
    def attributes(self):
        return {'data-ng-minlength': value}

    def alter_schema(self, schema, fqn):
        if schema['type'] != 'object':
            schema['minLength'] = self.value


class MaximumLength(Modifier):
    """
    Add a maximum value validation.
    """

    def __init__(self, value):
        """
        """
        self.value

    @property
    def attributes(self):
        return {'data-ng-maxlength': value}

    def alter_schema(self, schema, fqn):
        if schema['type'] != 'object':
            schema['maxLength'] = self.value
