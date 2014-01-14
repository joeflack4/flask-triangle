# -*- encoding: utf-8 -*-
"""
    flask_triangle.schema.format
    ----------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .natural import String


class Email(String):
    """
    """

    def __schema__(self):
        """
        """
        res = super(Email, self).__schema__()
        res['format'] = 'email'
        # because format support is optional :
        res['pattern'] = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-.])*$'
        return res