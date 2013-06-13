# -*- encoding: utf-8 -*-
"""
    flaskey_triangle.schema
    ---------------------

    Implements Schema.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
import collections


class Schema(dict):
    """
    This object is a custom dict with advanced methods to easily create a
    JSON-schema.
    """

    def __init__(self, init=None):
        self.dirty = True
        super(Schema, self).__init__(dict() if init is None else init)

    def compile(self):
        """Compile the "annotated" json-schema to a valid json-schema."""
        if self.dirty:
            self.apply_func(self.node_compile)
            self.dirty = False
        return self

    @staticmethod
    def __merge(d, u):
        for key, val in u.iteritems():
            if isinstance(val, collections.Mapping) and \
                isinstance(d.get(key, None), collections.Mapping):
                d[key] = Schema.__merge(d.get(key, {}), val)
            elif type(val) is list and type(d.get(key, None)) is list:
                d[key] = list(set(d.get(key, []) + val))
            else:
                d[key] = u[key]
        return d


    def merge(self, other):
        """
        Merge the current schema with another mapping object. This is a
        recursive merging.
        """
        self.dirty = True
        Schema.__merge(self, other)

    def apply_func(self, func, fqn=u''):
        """
        Apply a function to the current schema and its nested objects.

        :arg func: A custom function with the following signature :
                   ``my_func(schema, fqn)``. The first parameter will be the
                   processed object and the second its fully qualified name.
                   The FQN of the root object is an empty string.

        Apply_func will stop when an object is a leaf of the root schema or
        if the applied function return a ``True`` value.
        """
        self.dirty = True

        if func(self, fqn):
            return self

        for key, val in self.get(u'properties', dict()).items():
            val.apply_func(func, u'{}{}'.format(fqn, u'.{}'.format(key) 
                                                     if fqn else key))

        for key, val in self.get(u'patternProperties', dict()).items():
            val.apply_func(func, u'{}{}'.format(fqn, u'.*' if fqn else '*'))

        return self

    @staticmethod
    def node_compile(schema, fqn):
        """
        Some properties are annotated for an easier management from
        flask-triangle. This function, called by apply_func will transform
        annotations to true and valid json schema.
        """

        # anticipated return when dealing with pattern properties
        if fqn.endswith('*'):
            return

        pattern_properties = schema.get(u'patternProperties', dict())

        for key, val in schema.get(u'properties', dict()).items():
            pattern = val.get(u'asPatternProperty', None)
            if pattern is not None:
                pattern_properties[pattern] = val
                del val[u'asPatternProperty']
                del schema[u'properties'][key]
                if key in schema.get(u'required', list()):
                    schema[u'required'].remove(key)

        if len(pattern_properties):
            schema[u'patternProperties'] = pattern_properties

        if u'properties' in schema and not len(schema[u'properties']):
            del schema[u'properties']

        if u'required' in schema and not len(schema[u'required']):
            del schema[u'required']
