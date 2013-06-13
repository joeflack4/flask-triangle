# -*- encoding: utf-8 -*-
"""
"""


class Validator(object):
    """
    The base class for every validators.
    """

    def __init__(self):
        self.attributes = dict()

    def alter_schema(self, schema, fqn):
        return True
