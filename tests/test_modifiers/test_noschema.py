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

from flask_triangle.modifiers import NoSchema
from flask_triangle.schema import Schema


class TestRegexp(object):

    def setup(self):
        self.validator = NoSchema()

    def test_0(self):
        """
        When applied to an existing schema, an empty schema is returned.
        """
        schema = Schema({'type': 'object',
                         'properties': {'normal': Schema({'type': 'string'})},
                         'required': ['normal']})

        schema.apply_func(self.validator.alter_schema)
        assert_equal(len(schema), 0)
