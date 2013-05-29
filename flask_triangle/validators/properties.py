
# -*- encoding: utf-8 -*-
"""
flask_triangle.
"""


from flask_triangle.validators.common import Validator
from flask_triangle.types import Schema


class Properties(Validator):
    """
    Properties is a special validator. It is always called by any widget
    because it's in charge to build the json-schema skeleton.
    """

    alter_schema = (True, False, False)

    def __init__(self, binding, type_):
        """
        :arg binding: A string. The full name of the json bound value. (i.e. :
        'my.full.name')

        :arg type_: A string. A valid JSON type.
        """

        self.binding = binding
        self.type_ = type_

    def schema(self, **kwargs):

        root = Schema({u'type': u'object', u'properties': {}})

        parent = root
        for child in self.binding.split(u'.'):
            new = {child: {u'type': u'object', u'properties': {}}}
            parent.get(u'properties').update(new)
            parent = new.get(child)

        del parent[u'properties']
        parent[u'type'] = self.type_

        return root

