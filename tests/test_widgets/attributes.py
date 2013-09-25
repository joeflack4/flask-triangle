# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import flask

from flask_triangle import Triangle
from flask_triangle.widget import HtmlAttr
from nose.tools import assert_true, assert_equal, assert_false


class TestAttributes0(object):
    """
    One attribute to string.
    """

    def setup(self):
        pass

    def test_type(self):
        assert_true(issubclass(HtmlAttr, dict))

    def test_simple(self):
        assert_equal(unicode(HtmlAttr({'test': 'ok'})), 'test="ok"')

    def test_boolean_attr(self):
        assert_equal(unicode(HtmlAttr({'test': None})), 'test')

    def test_boolean_value0(self):
        assert_equal(unicode(HtmlAttr({'test': True})), 'test="true"')

    def test_boolean_value1(self):
        assert_equal(unicode(HtmlAttr({'test': False})), 'test="false"')

    def test_numeric_value(self):
        assert_equal(unicode(HtmlAttr({'test': 42})), 'test="42"')

    def test_camelcase_attr0(self):
        assert_equal(unicode(HtmlAttr({'camelCase': 'ok'})), 'camel-case="ok"')

    def test_camelcase_attr1(self):
        assert_equal(unicode(HtmlAttr({'camelCASE': 'ok'})), 'camel-case="ok"')

    def test_camelcase_attr2(self):
        assert_equal(unicode(HtmlAttr({'CAMELCase': 'ok'})), 'camel-case="ok"')

    def test_notcamelcase_attr0(self):
        assert_equal(unicode(HtmlAttr({'not-camel-case': 'ok'})),
                     'not-camel-case="ok"')

    def test_notcamelcase_attr1(self):
        assert_equal(unicode(HtmlAttr({'not_camel_case': 'ok'})),
                     'not_camel_case="ok"')

class TestAttributes1(object):
    """
    More than one attribute.
    """

    def setup(self):
        self.test = HtmlAttr(attr='value', boolean=None, camelCase=True)

    def test_simple(self):
        assert_equal(unicode(self.test),
                     'attr="value" boolean camel-case="true"')

    def test_collision(self):
        self.test['camel-case'] = 'only-one'
        assert_false('"only-one"' in unicode(self.test) and
                     '"true"' in unicode(self.test))

t = flask.render_template_string
class TestAttributesAngular(object):
    """
    Double bracketted attribute.
    """

    def setup(self):
        self.app = flask.Flask(__name__)

    def test_simple(self):
        test = HtmlAttr(attr='value|angular')
        #attributes are formated
        with self.app.test_request_context():
            assert_equal(t('{{a}}', a=unicode(test).format()),
                         'attr="{{value}}"')

    def test_complex(self):
        test = HtmlAttr(attr='''value|date: 'fullDate'|angular''')
        #attributes are formated
        with self.app.test_request_context():
            assert_equal(t('{{a}}', a=unicode(test).format()),
                         '''attr="{{value|date: 'fullDate'}}"''')


