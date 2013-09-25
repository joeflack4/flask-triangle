# -*- encoding: utf-8 -*-
"""
    tests.widgets.default.custom
    ----------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


from flask_triangle import Widget

from jsonschema import Draft3Validator
from nose.tools import assert_equal, assert_not_in, assert_in

class SimpleCustomWidget(Widget):

    html_template = '<tag {{widget.html_attributes}}></tag>'
    schema = {'type': 'string'}


class TestRendering(object):

    def test_0(self):
        """
        the {{widget.html_attributes}} renders all the html attributes correctly
        """
        widget = SimpleCustomWidget('bind', name='value')
        assert_in(unicode(widget.html_attributes), widget())


class TestSchema0(object):

    def setup(self):
        self.widget = SimpleCustomWidget('test')

    def test_0(self):
        """The schema is valid"""
        Draft3Validator.check_schema(self.widget.schema)

    def test_1(self):
        """
        The "leaf" of the schema is equal to the schema attribute of the class.
        """
        for k, v in SimpleCustomWidget.schema.iteritems():
            assert_equal(self.widget.schema['properties']['test'][k], v)


class TestSchema1(object):

    def setup(self):
        self.widget = SimpleCustomWidget('super.nested.test')

    def test_0(self):
        """The schema is valid"""
        Draft3Validator.check_schema(self.widget.schema)

    def test_1(self):
        """
        an object is created for each nesting level. The last one (the leaf)
        holds the class schema.
        """
        root = self.widget.schema
        for level in self.widget.bind.split('.'):
            assert_in(level, root['properties'])
            root = root['properties'][level]

    def test_2(self):
        """
        the "leaf" of the schema is equal to the schema attribute of the class.
        """
        root = self.widget.schema
        for level in self.widget.bind.split('.'):
            root = root['properties'][level]
        for k, v in SimpleCustomWidget.schema.iteritems():
            assert_equal(root[k], v)
