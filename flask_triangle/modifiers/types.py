# -*- encoding: utf-8 -*-
"""
    flask_triangle.validators.type
    ------------------------------

    Validators to modify and verify the return type of a widget.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from .modifier import Modifier


class AsOthertype(Modifier):
    """
    This class requires to be inherited and the class attribute `target_type` to
    be set.
    """

    def alter_schema(self, schema, bind):
        """
        Modify the type if the node exists and is not an 'object'.
        """

        node = schema.get(bind)
        if node is not None and node._type != 'object':
            node._type = self.target_type


class AsBoolean(AsOthertype):
    """
    The value bound to the widget is a boolean.
    """
    target_type = 'boolean'


class AsInteger(AsOthertype):
    """
    The value bound to the widget is an integer.
    """
    target_type = 'integer'