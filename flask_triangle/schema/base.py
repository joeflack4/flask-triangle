# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.base
    --------------------------

    The base type for all types used in a JSON Schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


class BaseType(object):

    def __init__(self, type_,
                 enum=None, all_of=None, any_of=None, one_of=None, is_not=None):

        # This will override the computed schema if not None
        self._custom_schema = None

        self.type = type_
        self.enum = enum
        self.all_of = all_of
        self.any_of = any_of
        self.one_of = one_of
        self.is_not = is_not

    @property
    def schema(self):
        """
        Return the schema.
        """
        if self._custom_schema is None:
            return self.__schema__()
        return self._custom_schema

    @schema.setter
    def schema(self, value):
        """
        Set a custom schema to override the one computed.
        """
        self._custom_schema = value

    def cache(self, active=True):
        """
        Cache the generated schema to avoid its recomputation on each access.
        If `active` is False, the cache is unset.

        Beware ! Unset the cache will delete any custom schema.
        """
        if active:
            self._custom_schema = self.__schema__()
        else:
            self._custom_schema = None

    def __schema__(self):
        """
        Generate the JSON schema.
        """

        res = {'type': self.type}

        if self.enum is not None: res['enum'] = self.enum
        if self.all_of is not None: res['allOf'] = self.all_of
        if self.any_of is not None: res['anyOf'] = self.any_of
        if self.one_of is not None: res['oneOf'] = self.any_of
        if self.is_not is not None: res['not'] = self.is_not

        return res