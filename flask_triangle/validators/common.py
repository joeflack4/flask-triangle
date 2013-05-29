# -*- encoding: utf-8 -*-
"""
"""


from flask_triangle.types import Schema, Attributes


class Validator(object):
    """
    The base class for every validators.

    This one does nothing and is not intended to be used as is.
    """

    alter_schema = (False, False, False)

    def attributes(self):
        return Attributes()

    def schema(self):
        return Schema()
