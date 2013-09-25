# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from nose.tools import assert_equal

from flask_triangle.modifiers import AsBoolean
from flask_triangle.schema import Schema


class TestAsBoolean(object):

    def setup(self):
        self.validator = AsBoolean()

    def test_3(self):
        """
        Modify the type of the leaf object.
        """
        schema = Schema({'type': 'object',
                         'properties': {'normal': Schema({'type': 'string'})},
                         'required': ['normal']})

        schema.apply_func(self.validator.alter_schema)

        assert_equal('boolean', schema['properties']['normal']['type'])
