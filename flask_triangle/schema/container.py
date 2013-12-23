# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.container
    -------------------------------

    Include all the primitive types as defined in the JSON schema draft and
    which are container type.

    http://tools.ietf.org/html/draft-zyp-json-schema-04

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import copy, jsonschema

from .base import BaseType
from ..exc import MergeError


class PropertyCollection(dict):
    """
    An internal class to enhance the default dict with advanced features such
    as the conversion of dict of python objects to dict of schema properties.
    """

    def add(self, key, value):
        self[key] = value

    def schema(self):
        return dict([(k, v.schema) for k, v in self.items()])


class Object(BaseType):
    """
    The object is the base container. It has named properties, pattern
    properties and
    """

    def __init__(self, min_properties=0, max_properties=None, required=None,
                 additional_properties=True, **kwargs):

        super(Object, self).__init__('object', **kwargs)

        # Describe the behavior of the object regarding the number of its
        # optional properties
        self.max_properties = max_properties
        self.min_properties = min_properties
        self.additional_properties = additional_properties

        # Declared properties
        self.properties = PropertyCollection()
        self.pattern_properties = PropertyCollection()

        # Required properties
        if required is None: self.required = list()

    def merge(self, other):
        """
        Merge another schema in this one.
        """
        if not issubclass(type(other), Object):
            raise MergeError('Only container objects can be merged together.')

        # For each properties of the object. If the subproperties is an
        # object try to merge it, else overwrite it with the new value.
        for k, v in other.properties.items():
            if not (k in self.properties and issubclass(type(v), Object)):
                self.properties[k] = copy.deepcopy(v)
            elif issubclass(type(self.properties[k]), Object):
                self.properties[k].merge(v)
            else:
                self.properties[k] = copy.deepcopy(v)

        for k, v in other.pattern_properties.items():
            if not (k in self.pattern_properties and issubclass(type(v), Object)):
                self.pattern_properties[k] = copy.deepcopy(v)
            elif issubclass(type(self.pattern_properties[k]), Object):
                self.pattern_properties[k].merge(v)
            else:
                self.pattern_properties[k] = copy.deepcopy(v)

        self.required = list(set(self.required + other.required))

        # reset the schema
        self.schema = None

    def get(self, name):
        """
        Return the property `name`.
        If the property does not exist, this method return `None`.
        """
        name += '.' # hack to always unpack two values
        local, child = name.split('.', 1)

        res = self.properties.get(local)
        if child and res is not None:   # if there is a child
            return res.get(child[:-1])  # remove the appended dot
        return res


    def validate(self, json):
        """
        Validate the `json` against the current JSON Schema.
        """
        jsonschema.validate(json, self.schema)

    def __schema__(self):

        res = super(Object, self).__schema__()

        if len(self.required): res['required'] = list(set(self.required))

        if self.min_properties:
            res['minProperties'] = self.min_properties
        if self.max_properties is not None:
            res['maxProperties'] = self.max_properties
        if self.additional_properties is not True:
            res['additionalProperties'] = self.additional_properties
        if len(self.properties):
            res['properties'] = self.properties.schema()
        if len(self.pattern_properties):
            res['patternProperties'] = self.pattern_properties.schema()

        return res


class Schema(Object):
    """
    A specialized Object container with meta information, used as root object
    of a Schema.
    """

    def __init__(self, title=None, description=None, **kwargs):

        super(Schema, self).__init__(**kwargs)
        self.title = title
        self.description = description

    def __schema__(self):

        res = super(Schema, self).__schema__()

        if self.title is not None:
            res['title'] = self.title
        if self.description is not None:
            res['description'] = self.description

        return res