# -*- encoding: utf-8 -*-
"""
    test.schema.container
    ---------------------

    Common test for container classes.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jsonschema
from nose.tools import assert_is, assert_in, assert_not_in, assert_equal, raises
from flask_triangle.schema import Object, String
from flask_triangle.exc import MergeError



class CheckContainerProperties(object):
    """
    Test the validity and the features of a schema.
    """

    def test_empty(self):
        """
        An empty container is valid.
        """
        jsonschema.Draft4Validator.check_schema(self.item.schema)

    def test_add_property0(self):
        """
        Add a property.
        """
        self.item.properties.add('toto', Object())
        assert_in('toto', self.item.schema['properties'])

    def test_add_property1(self):
        """
        The schema is valid when a property is added.
        """
        self.item.properties.add('toto', Object())
        jsonschema.Draft4Validator.check_schema(self.item.schema)

    def test_add_pattern_property0(self):
        """
        Add a property.
        """
        self.item.pattern_properties.add('^test$', Object())
        assert_in('^test$', self.item.schema['patternProperties'])

    def test_add_pattern_property1(self):
        """
        The schema is valid when a property is added.
        """
        self.item.pattern_properties.add('^test$', Object())
        jsonschema.Draft4Validator.check_schema(self.item.schema)

    def test_min_properties(self):
        self.item.min_properties = 1
        assert_in('minProperties', self.item.schema)
        assert_equal(self.item.schema['minProperties'], 1)

    def test_max_properties(self):
        self.item.max_properties = 1
        assert_in('maxProperties', self.item.schema)
        assert_equal(self.item.schema['maxProperties'], 1)

    def test_required0(self):
        """
        empty required list should not appear.
        """
        self.item.required = []
        assert_not_in('required', self.item.schema)

    def test_required1(self):
        """
        empty required list should not appear.
        """
        self.item.required = ['some', 'value']
        assert_in('required', self.item.schema)
        assert_equal(len(self.item.schema['required']), 2)


class CheckDataValidation(object):
    """
    Test the validation of data.
    """

    def test_accept_all(self):
        """
        Successful validation raises no error.
        """
        self.item.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_accept_none0(self):
        """
        Should raise a ValidationError.
        """
        self.item.additional_properties = False # The item object does not have
                                                # any properties.
        self.item.validate({'test': 'fail'})

    def test_accept_none1(self):
        """
        Should not raise a Validation error if the json object if empty.
        """
        self.item.additional_properties = False
        self.item.validate({})

    @raises(jsonschema.ValidationError)
    def test_required0(self):
        """
        Should fail if the required property is missing.
        """
        self.item.required.append('test')
        self.item.validate({'other': 'fail'})

    def test_required1(self):
        """
        Should not fail if the required property is present.
        """
        self.item.required.append('test')
        self.item.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_patternprop0(self):
        """
        Should raise an error if the pattern property is missing.
        """
        self.item.pattern_properties.add('^test$', Object())
        self.item.additional_properties = False
        self.item.required.append('test')
        self.item.validate({'fail': {}})

    def test_patternprop1(self):
        """
        Should succeed if the pattern property (and only it) is present.
        """
        self.item.pattern_properties.add('^test$', Object())
        self.item.additional_properties = False
        self.item.required.append('test')
        self.item.validate({'test': {}})


class CheckMerging(object):
    """
    Test the merging of the object.
    """

    def test_merge0(self):
        """
        The merged object should append its properties in the first.
        """
        self.a.properties.add('first', Object())
        self.b.properties.add('second', Object())
        self.a.merge(self.b)

        assert_in('first', self.a.properties)
        assert_in('second', self.a.properties)

    def test_merge1(self):
        """
        The merge propagate through nested object.
        """
        self.a.properties.add('nested', Object())
        self.a.properties['nested'].properties.add('first', Object())

        self.b.properties.add('nested', Object())
        self.b.properties['nested'].properties.add('second', Object())

        self.a.merge(self.b)

        assert_in('first', self.a.properties['nested'].properties)
        assert_in('second', self.a.properties['nested'].properties)

    def test_merge2(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        self.a.properties.add('test', Object())
        self.b.properties.add('test', String())
        self.a.merge(self.b)

        assert_equal('string', self.a.schema['properties']['test']['type'])

    def test_merge3(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        self.a.properties.add('test', String())
        self.b.properties.add('test', Object())
        self.a.merge(self.b)

        assert_equal('object', self.a.schema['properties']['test']['type'])

    def test_merge4(self):
        """
        The merge will update the required list by merging it if necessary.
        """
        self.a.properties.add('first', Object())
        self.a.required.append('first')
        self.b.properties.add('second', Object())
        self.b.required.append('second')
        self.a.merge(self.b)

        assert_in('first', self.a.schema['required'])
        assert_in('second', self.a.schema['required'])

    def test_merge5(self):
        """
        No duplicate fields in the required.
        """
        self.a.properties.add('test', String())
        self.a.required.append('test')
        self.b.properties.add('test', Object())
        self.b.required.append('test')
        self.a.merge(self.b)

        assert_equal(len(self.a.schema['required']), 1)


    def test_merge6(self):
        """
        The merged object should append its properties in the first.
        """
        self.a.pattern_properties.add('first', Object())
        self.b.pattern_properties.add('second', Object())
        self.a.merge(self.b)

        assert_in('first', self.a.pattern_properties)
        assert_in('second', self.a.pattern_properties)

    def test_merge7(self):
        """
        The merge propagate through nested object.
        """
        self.a.pattern_properties.add('nested', Object())
        self.a.pattern_properties['nested'].properties.add('first', Object())

        self.b.pattern_properties.add('nested', Object())
        self.b.pattern_properties['nested'].properties.add('second', Object())

        self.a.merge(self.b)

        assert_in('first', self.a.pattern_properties['nested'].properties)
        assert_in('second', self.a.pattern_properties['nested'].properties)

    def test_merge8(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        self.a.pattern_properties.add('test', Object())
        self.b.pattern_properties.add('test', String())
        self.a.merge(self.b)

        assert_equal('string',
                     self.a.schema['patternProperties']['test']['type'])

    def test_merge9(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        self.a.pattern_properties.add('test', String())
        self.b.pattern_properties.add('test', Object())
        self.a.merge(self.b)

        assert_equal('object',
                     self.a.schema['patternProperties']['test']['type'])

    @raises(MergeError)
    def test_merge_error(self):
        """
        A container cannot be merged with a non container object.
        """
        self.a.merge(String())


class CheckPropertyAccess(object):
    """
    test the children access
    """

    def test_get_simple(self):
        """
        get('test') should return the property named 'test'.
        """
        target = String()
        self.item.properties.add('test', target)
        assert_is(self.item.get('test'), target)

    def test_get_none(self):
        """
        get('missing_property') should return `None`.
        """
        assert_is(self.item.get('missing_property'), None)

    def test_get_nested(self):
        """
        get('nested.test') should return the property 'test' in the child object
        'nested'.
        """
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        self.item.properties.add('nested', nested)

        assert_is(self.item.get('nested.test'), target)

    def test_get_erroneous0(self):
        """
        get('nested.') should return `None`
        """
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        self.item.properties.add('nested', nested)

        assert_is(self.item.get('nested.'), None)

    def test_get_erroneous1(self):
        """
        get('.nested.test') should return `None`
        """
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        self.item.properties.add('nested', nested)

        assert_is(self.item.get('.nested.test'), None)