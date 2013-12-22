# -*- encoding: utf-8 -*-
"""
    test.schema
    -----------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import jsonschema
from nose.tools import (assert_not_in, assert_in, assert_equal, assert_true,
                        assert_is, raises)

from flask_triangle.exc import MergeError
from flask_triangle.schema import Schema, Object, String


class TestSchemaType(object):
    """
    Test the object hierarchy of Schema / Object
    """

    def test_subclass(self):
        """
        A Schema is a subclass of the Object class.
        """
        assert_true(issubclass(Schema, Object))

    def test_schema_title(self):
        """
        The schema has a specific title property.
        """
        assert_equal('ok', Schema(title='ok').schema['title'])

    def test_schema_description(self):
        """
        The schema has a specific title property.
        """
        assert_equal('ok', Schema(description='ok').schema['description'])


class TestSchema0(object):
    """
    Test the validity and the features of a schema.
    """

    def setup(self):
        self.root = Schema(title='test', description='A test schema.')

    def test_empty(self):
        """
        An empty schema is valid.
        """
        jsonschema.Draft4Validator.check_schema(self.root.schema)

    def test_update(self):
        """
        The schema is computed at the runtime and is mutable.
        """
        assert_not_in('required', self.root.schema)
        self.root.required.append('test')   # add test to the required fields
        assert_in('test', self.root.schema['required'])

    def test_cache_set(self):
        """
        The schema can be cached.
        """
        assert_not_in('required', self.root.schema)
        self.root.cache()
        self.root.required.append('test')
        assert_not_in('required', self.root.schema)

    def test_cache_unset(self):
        """
        The cache can be unset.
        """
        assert_not_in('required', self.root.schema)
        self.root.cache()
        self.root.required.append('test')
        self.root.cache(False)
        assert_in('test', self.root.schema['required'])

    def test_override_schema(self):
        """
        The computed schema can be overridden with a custom schema.
        """
        assert_not_in('properties', self.root.schema)
        self.root.schema = {'type': 'object',
                            'properties': {'custom': {'type': 'boolean'}}}
        assert_in('properties', self.root.schema)

    def test_add_property0(self):
        """
        Add a property.
        """
        self.root.properties.add('toto', Object())
        assert_in('toto', self.root.properties)

    def test_add_property1(self):
        """
        The schema is valid when a property is added.
        """
        self.root.properties.add('toto', Object())
        jsonschema.Draft4Validator.check_schema(self.root.schema)

    def test_add_pattern_property0(self):
        """
        Add a property.
        """
        self.root.pattern_properties.add('^test$', Object())
        assert_in('^test$', self.root.pattern_properties)

    def test_add_pattern_property1(self):
        """
        The schema is valid when a property is added.
        """
        self.root.pattern_properties.add('^test$', Object())
        jsonschema.Draft4Validator.check_schema(self.root.schema)


class TestSchema1(object):
    """
    Test the validation of data.
    """

    def setup(self):
        self.root = Schema(title='test', description='A test schema.')

    def test_accept_all(self):
        """
        Successful validation raises no error.
        """
        self.root.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_accept_none0(self):
        """
        Should raise a ValidationError.
        """
        self.root.additional_properties = False # The root object does not have
                                                # any properties.
        self.root.validate({'test': 'fail'})

    def test_accept_none1(self):
        """
        Should not raise a Validation error if the json object if empty.
        """
        self.root.additional_properties = False
        self.root.validate({})

    @raises(jsonschema.ValidationError)
    def test_required0(self):
        """
        Should fail if the required property is missing.
        """
        self.root.required.append('test')
        self.root.validate({'other': 'fail'})

    def test_required1(self):
        """
        Should not fail if the required property is present.
        """
        self.root.required.append('test')
        self.root.validate({'test': 'ok'})

    @raises(jsonschema.ValidationError)
    def test_patternprop0(self):
        """
        Should raise an error if the pattern property is missing.
        """
        self.root.pattern_properties.add('^test$', Object())
        self.root.additional_properties = False
        self.root.required.append('test')
        self.root.validate({'fail': {}})

    def test_patternprop1(self):
        """
        Should succeed if the pattern property (and only it) is present.
        """
        self.root.pattern_properties.add('^test$', Object())
        self.root.additional_properties = False
        self.root.required.append('test')
        self.root.validate({'test': {}})


class TestSchema2(object):
    """
    Test the merging of the object.
    """

    def test_merge0(self):
        """
        The merged object should append its properties in the first.
        """
        a = Schema()
        a.properties.add('first', Object())
        b = Schema()
        b.properties.add('second', Object())
        a.merge(b)

        assert_in('first', a.properties)
        assert_in('second', a.properties)

    def test_merge1(self):
        """
        The merge propagate through nested object.
        """
        a = Schema()
        a.properties.add('nested', Object())
        a.properties['nested'].properties.add('first', Object())

        b = Schema()
        b.properties.add('nested', Object())
        b.properties['nested'].properties.add('second', Object())

        a.merge(b)

        assert_in('first', a.properties['nested'].properties)
        assert_in('second', a.properties['nested'].properties)

    def test_merge2(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        a = Schema()
        a.properties.add('test', Object())
        b = Schema()
        b.properties.add('test', String())
        a.merge(b)

        assert_equal('string', a.properties['test'].type)

    def test_merge3(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        a = Schema()
        a.properties.add('test', String())
        b = Schema()
        b.properties.add('test', Object())
        a.merge(b)

        assert_equal('object', a.properties['test'].type)

    def test_merge4(self):
        """
        The merge will update the required list by merging it if necessary.
        """
        a = Schema()
        a.properties.add('first', Object())
        a.required.append('first')
        b = Schema()
        b.properties.add('second', Object())
        b.required.append('second')
        a.merge(b)

        assert_in('first', a.required)
        assert_in('second', a.required)

    def test_merge5(self):
        """
        No duplicate fields in the required.
        """
        a = Schema()
        a.properties.add('test', String())
        a.required.append('test')
        b = Schema()
        b.properties.add('test', Object())
        b.required.append('test')
        a.merge(b)

        assert_equal(len(a.required), 1)


    def test_merge6(self):
        """
        The merged object should append its properties in the first.
        """
        a = Schema()
        a.pattern_properties.add('first', Object())
        b = Schema()
        b.pattern_properties.add('second', Object())
        a.merge(b)

        assert_in('first', a.pattern_properties)
        assert_in('second', a.pattern_properties)

    def test_merge7(self):
        """
        The merge propagate through nested object.
        """
        a = Schema()
        a.pattern_properties.add('nested', Object())
        a.pattern_properties['nested'].properties.add('first', Object())

        b = Schema()
        b.pattern_properties.add('nested', Object())
        b.pattern_properties['nested'].properties.add('second', Object())

        a.merge(b)

        assert_in('first', a.pattern_properties['nested'].properties)
        assert_in('second', a.pattern_properties['nested'].properties)

    def test_merge8(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        a = Schema()
        a.pattern_properties.add('test', Object())
        b = Schema()
        b.pattern_properties.add('test', String())
        a.merge(b)

        assert_equal('string', a.pattern_properties['test'].type)

    def test_merge9(self):
        """
        The merge act as an update if two properties with the same name aren't
        containers.
        """
        a = Schema()
        a.pattern_properties.add('test', String())
        b = Schema()
        b.pattern_properties.add('test', Object())
        a.merge(b)

        assert_equal('object', a.pattern_properties['test'].type)

    @raises(MergeError)
    def test_merge_error(self):
        """
        A container cannot be merged with a non container object.
        """
        a = Schema()
        b = String()
        a.merge(b)

class TestSchema3(object):
    """
    test additional attributes of an object
    """

    def test_min_properties(self):
        root = Schema(min_properties=1)
        assert_in('minProperties', root.schema)
        assert_equal(root.schema['minProperties'], 1)

    def test_max_properties(self):
        root = Schema(max_properties=1)
        assert_in('maxProperties', root.schema)
        assert_equal(root.schema['maxProperties'], 1)

class TestSchemaPropertyAcces(object):
    """
    test the children access
    """

    def test_get_simple(self):
        """
        get('test') should return the property named 'test'.
        """
        target = String()
        a = Schema()
        a.properties.add('test', target)

        assert_is(a.get('test'), target)

    def test_get_none(self):
        """
        get('missing_property') should return `None`.
        """
        a = Schema()
        assert_is(a.get('missing_property'), None)

    def test_get_nested(self):
        """
        get('nested.test') should return the property 'test' in the child object
        'nested'.
        """
        a = Schema()
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        a.properties.add('nested', nested)

        assert_is(a.get('nested.test'), target)

    def test_get_erroneous0(self):
        """
        get('nested.') should return `None`
        """
        a = Schema()
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        a.properties.add('nested', nested)

        assert_is(a.get('nested.'), None)

    def test_get_erroneous1(self):
        """
        get('.nested.test') should return `None`
        """
        a = Schema()
        target = String()
        nested = Object()

        nested.properties.add('test', target)
        a.properties.add('nested', nested)

        assert_is(a.get('.nested.test'), None)
