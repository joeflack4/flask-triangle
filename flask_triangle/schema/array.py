# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.array
    ---------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .base import BaseType


class Array(BaseType):
    """
    """

    def __init__(self, items,
                 max_items=0, min_items=0, unique_items=False,
                 **kwargs):
        super(Array, self).__init__('array', **kwargs)
        self.items = items
        self.min_items=min_items
        self.max_items=max_items
        self.unique_items=unique_items

    def __schema__(self):

        res = super(Array, self).__schema__()

        if issubclass(type(self.items), BaseType):
            res['items'] = self.items.__schema__()
        elif self.items is not None:
            res['items'] = [item.__schema__() for item in self.items]

        if self.min_items:
            res['minItems'] = self.min_items
        if self.max_items:
            res['maxItems'] = self.max_items
        if self.unique_items:
            res['uniqueItems'] = self.unique_items

        return res