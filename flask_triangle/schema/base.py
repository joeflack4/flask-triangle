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

        self._custom_schema = None  # see schema() property for more information

        self._type = type_
        self.is_not = is_not

        if all_of is None:
            self.all_of = []
        else:
            self.all_of = all_of

        if any_of is None:
            self.any_of = []
        else:
            self.any_of = any_of

        if one_of is None:
            self.one_of = []
        else:
            self.one_of = one_of

        if enum is None:
            self.enum = []
        else:
            self.enum = enum

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

        res = {'type': self._type}

        if len(self.enum): res['enum'] = self.enum
        if len(self.all_of): res['allOf'] = [i.schema for i in self.all_of]
        if len(self.any_of): res['anyOf'] = [i.schema for i in self.any_of]
        if len(self.one_of): res['oneOf'] = [i.schema for i in self.one_of]

        if self.is_not is not None: res['not'] = self.is_not.schema

        return res