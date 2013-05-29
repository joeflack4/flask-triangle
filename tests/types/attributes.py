# -*- encoding: utf-8 -*-


import re
from flask_triangle.types import Attributes

from nose.tools import assert_true, assert_equal, assert_in


class TestAttributes(object):

    def test_attributes_type(self):
        '''Attributes is an inherited dict class.'''
        assert_true(issubclass(Attributes, dict))

    def test_attributes_callable(self):
        '''An Attributes instance is callable.'''
        assert_in('__call__', dir(Attributes()))

    def test_attributes_call_empty(self):
        '''Calling an empty attribute instance will return an empty string.'''
        instance = Attributes()
        assert_equal(u'', instance())

    def test_attributes_call_nonboolean(self):
        '''
            Calling an Attributes instance with a nonboolean attribute will
            return the expected string.
        '''
        instance = Attributes({u'test' : u'ok'})
        assert_equal(u'test="ok"', instance())

    def test_attributes_call_boolean(self):
        '''
            Calling an Attributes instance with a boolean attribute will
            return the expected string.
        '''
        instance = Attributes({u'test' : None})
        assert_equal(u'test', instance())

    def test_attributes_call_mixed(self):
        '''
            Calling an Attributes instance with mixed values of boolean and
            nonboolean attributes will return a well formated string.
        '''
        instance = Attributes({u'test0': None, u'test1': u'ok'})
        regex = (r'^(([^\s="]+="[^"]+")?( [^\s="]+="[^"]+")*)?(([^\s="]+)?( [^'
                 r'\s="]+)*)?$')
        assert_true(re.match(regex, instance()))
