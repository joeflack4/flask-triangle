# -*- encoding: utf-8 -*-
"""
    flask_triangle.modifiers.multiple
    ---------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from flask_triangle.schema import Schema, Array
from .modifier import Modifier


class Multiple(Modifier):
    """
    Add a constraint allowing more than one entry to be selected in a `select`
    widget. This will affect the attributes of HTML widget and the validation
    json schema altogether. However, this does not enable any client validation.
    """

    def __init__(self, unique_items=False, max_items=0, min_items=0):
        self.unique_items = unique_items
        self.max_items = max_items
        self.min_items = min_items

    def alter_html_attr(self, html_attrs):
        html_attrs.update({'multiple': None})

    def alter_schema(self, schema, bind):

        path = bind.rsplit('.', 1)
        if len(path) == 2:
            parent = schema.get(path[0])
            child_name = path[1]
        else:
            parent = schema
            child_name = path[0]

        target = schema.get(bind)
        parent.properties.add(child_name, Array(target,
                                                min_items=self.min_items,
                                                max_items=self.max_items,
                                                unique_items=self.unique_items))