# -*- encoding: utf-8 -*-
"""
    test.forms.validation
    ---------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle import Form
from flask_triangle.widgets.standard import TextInput
from nose.tools import raises

import jsonschema


class MyForm(Form):
    """
    A custom form for testing purpose.
    """
    entry1 = TextInput('form.entry1')
    entry0 = TextInput('form.entry0')


class TestSimpleValidation(object):

    def setup(self):

        self.form = MyForm('test')

    def test_direct_validation(self):
        """
        Use the schema to validate input data.
        """
        self.form.schema.validate({'form': {'entry0': 'ok',
                                            'entry1': 'ok'}})

    @raises(jsonschema.ValidationError)
    def test_direct_validation_failure(self):
        """
        Fail with using the schema to validate input data.
        """
        self.form.schema.validate({'form': {'entry0': 0}})

    @raises(jsonschema.ValidationError)
    def test_strict(self):
        """
        unexpected properties raise error.
        """
        self.form.schema.validate({'other': 'fail'})

    @raises(jsonschema.ValidationError)
    def test_recursive_strict(self):
        """
        unexpected properties raise error. (recursively)
        """
        self.form.schema.validate({'form': {'other': 'fail'}})


class TestUnstrictValidation(object):

    def setup(self):

        self.form = MyForm('test', strict=False)

    def test_direct_validation(self):
        """
        Use the schema to validate input data.
        """
        self.form.schema.validate({'form': {'entry0': 'ok',
                                            'entry1': 'ok'}})

    @raises(jsonschema.ValidationError)
    def test_direct_validation_failure(self):
        """
        Fail with using the schema to validate input data.
        """
        self.form.schema.validate({'form': {'entry0': 0}})

    def test_unstrict(self):
        """
        unexpected fields doesn't raise any error.
        """
        self.form.schema.validate({'other': 'ok'})


class TestRootValidation(object):

    def setup(self):

        self.form = MyForm('test', root='form')

    def test_validation0(self):
        """
        """
        self.form.schema.validate({'entry0': 'ok',
                                   'entry1': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_validation1(self):
        """
        """
        self.form.schema.validate({'form': {'entry0': 'ok',
                                            'entry1': 'ok'}})
