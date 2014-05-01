# -*- encoding: utf-8 -*-
"""
    test.schema.natural
    -------------------

    Each test is suffixed by a code indicating what is tested :

        - vs   : validiation test of the schema
        - vi   : validation test with valid input
        - bi   : validation test with invalid input
        - json : json rendering of the schema

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import unicode_literals
from __future__ import absolute_import

from six import text_type
from flask_triangle.schema import String, Integer, Number, Boolean

import unittest, jsonschema


class TestString(unittest.TestCase):

    def test_vs(self):

        ref = String()
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_vi(self):

        ref = String()
        jsonschema.validate('test ok !', ref.schema())

    def test_bi(self):

        ref = String()
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(0, ref.schema())

    def test_json(self):

        ref = String()
        self.assertEqual('{"type": "string"}', text_type(ref))

    def test_minlength_vs(self):

        ref = String(min_length=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_minlength_vi(self):

        ref = String(min_length=5)
        jsonschema.validate('test ok !', ref.schema())

    def test_minlength_bi(self):

        ref = String(min_length=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('fail', ref.schema())

    def test_minlength_json(self):

        ref = String(min_length=5)
        self.assertEqual('{"minLength": 5, "type": "string"}', text_type(ref))

    def test_maxlength_vs(self):

        ref = String(max_length=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_maxlength_vi(self):

        ref = String(max_length=5)
        jsonschema.validate('ok!', ref.schema())

    def test_maxlength_bi(self):

        ref = String(max_length=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('failure', ref.schema())

    def test_maxlength_json(self):

        ref = String(max_length=5)
        self.assertEqual('{"maxLength": 5, "type": "string"}', text_type(ref))

    def test_pattern_vs(self):

        ref = String(pattern='^[A-Z]*$')
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_pattern_vi(self):

        ref = String(pattern='^[A-Z]*$')
        jsonschema.validate('OK', ref.schema())

    def test_pattern_bi(self):

        ref = String(pattern='^[A-Z]*$')
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('fail', ref.schema())

    def test_pattern_json(self):

        ref = String(pattern='^[A-Z]*$')
        self.assertEqual('{"pattern": "^[A-Z]*$", "type": "string"}', text_type(ref))


class TestInteger(unittest.TestCase):

    def test_vs(self):

        ref = Integer()
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_vi(self):

        ref = Integer()
        jsonschema.validate(1, ref.schema())

    def test_bi(self):

        ref = Integer()
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('fail!', ref.schema())

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(1.1, ref.schema())

    def test_json(self):

        ref = Integer()
        self.assertEqual('{"type": "integer"}', text_type(ref))


    def test_multipleof_vs(self):

        ref = Integer(multiple_of=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_multipleof_vi(self):

        ref = Integer(multiple_of=5)
        jsonschema.validate(10, ref.schema())

    def test_multipleof_bi(self):

        ref = Integer(multiple_of=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(3, ref.schema())

    def test_multipleof_json(self):

        ref = Integer(multiple_of=5)
        self.assertEqual('{"multipleOf": 5, "type": "integer"}', text_type(ref))

    def test_minimum_vs(self):

        ref = Integer(minimum=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_minimum_vi(self):

        ref = Integer(minimum=5)
        jsonschema.validate(10, ref.schema())

    def test_minimum_bi(self):

        ref = Integer(minimum=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(3, ref.schema())

    def test_minimum_json(self):

        ref = Integer(minimum=5)
        self.assertEqual('{"minimum": 5, "type": "integer"}', text_type(ref))

    def test_maximum_vs(self):

        ref = Integer(maximum=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_maximum_vi(self):

        ref = Integer(maximum=5)
        jsonschema.validate(3, ref.schema())

    def test_maximum_bi(self):

        ref = Integer(maximum=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(10, ref.schema())

    def test_maximum_json(self):

        ref = Integer(maximum=5)
        self.assertEqual('{"maximum": 5, "type": "integer"}', text_type(ref))

    def test_exc_minimum_vs(self):

        ref = Integer(minimum=5, exclusive_minimum=True)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_exc_minimum_vi(self):

        ref = Integer(minimum=5, exclusive_minimum=True)
        jsonschema.validate(10, ref.schema())

    def test_exc_minimum_bi(self):

        ref = Integer(minimum=5, exclusive_minimum=True)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(5, ref.schema())

    def test_exc_minimum_json(self):

        ref = Integer(minimum=5, exclusive_minimum=True)
        self.assertEqual(
            '{"exclusiveMinimum": true, "minimum": 5, "type": "integer"}',
            text_type(ref)
        )

    def test_exc_maximum_vs(self):

        ref = Integer(maximum=5, exclusive_maximum=True)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_exc_maximum_vi(self):

        ref = Integer(maximum=5, exclusive_maximum=True)
        jsonschema.validate(3, ref.schema())

    def test_exc_maximum_bi(self):

        ref = Integer(maximum=5, exclusive_maximum=True)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(5, ref.schema())

    def test_exc_maximum_json(self):

        ref = Integer(maximum=5, exclusive_maximum=True)
        self.assertEqual(
            '{"exclusiveMaximum": true, "maximum": 5, "type": "integer"}',
            text_type(ref)
        )


class TestNumber(unittest.TestCase):

    def test_vs(self):

        ref = Number()
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_vi(self):

        ref = Number()
        jsonschema.validate(1, ref.schema())
        jsonschema.validate(1.1, ref.schema())

    def test_bi(self):

        ref = Number()
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('fail!', ref.schema())

    def test_json(self):

        ref = Number()
        self.assertEqual('{"type": "number"}', text_type(ref))

    def test_multipleof_vs(self):

        ref = Number(multiple_of=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_multipleof_vi(self):

        ref = Number(multiple_of=5)
        jsonschema.validate(10, ref.schema())

    def test_multipleof_bi(self):

        ref = Number(multiple_of=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(10.000001, ref.schema())

    def test_multipleof_json(self):

        ref = Number(multiple_of=5)
        self.assertEqual('{"multipleOf": 5, "type": "number"}', text_type(ref))

    def test_minimum_vs(self):

        ref = Number(minimum=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_minimum_vi(self):

        ref = Number(minimum=5)
        jsonschema.validate(5, ref.schema())

    def test_minimum_bi(self):

        ref = Number(minimum=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(4.9999, ref.schema())

    def test_minimum_json(self):

        ref = Number(minimum=5)
        self.assertEqual('{"minimum": 5, "type": "number"}', text_type(ref))

    def test_maximum_vs(self):

        ref = Number(maximum=5)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_maximum_vi(self):

        ref = Number(maximum=5)
        jsonschema.validate(3, ref.schema())

    def test_maximum_bi(self):

        ref = Number(maximum=5)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(5.000001, ref.schema())

    def test_maximum_json(self):

        ref = Number(maximum=5)
        self.assertEqual('{"maximum": 5, "type": "number"}', text_type(ref))

    def test_exc_minimum_vs(self):

        ref = Number(minimum=5, exclusive_minimum=True)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_exc_minimum_vi(self):

        ref = Number(minimum=5, exclusive_minimum=True)
        jsonschema.validate(5.000001, ref.schema())

    def test_exc_minimum_bi(self):

        ref = Number(minimum=5, exclusive_minimum=True)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(5, ref.schema())

    def test_exc_minimum_json(self):

        ref = Number(minimum=5, exclusive_minimum=True)
        self.assertEqual(
            '{"exclusiveMinimum": true, "minimum": 5, "type": "number"}',
            text_type(ref)
        )

    def test_exc_maximum_vs(self):

        ref = Number(maximum=5, exclusive_maximum=True)
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_exc_maximum_vi(self):

        ref = Number(maximum=5, exclusive_maximum=True)
        jsonschema.validate(4.99999, ref.schema())

    def test_exc_maximum_bi(self):

        ref = Number(maximum=5, exclusive_maximum=True)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(5, ref.schema())

    def test_exc_maximum_json(self):

        ref = Number(maximum=5, exclusive_maximum=True)
        self.assertEqual(
            '{"exclusiveMaximum": true, "maximum": 5, "type": "number"}',
            text_type(ref)
        )


class TestBoolean(unittest.TestCase):

    def test_vs(self):

        ref = Boolean()
        jsonschema.Draft4Validator.check_schema(ref.schema())

    def test_vi(self):

        ref = Boolean()
        jsonschema.validate(False, ref.schema())

    def test_bi(self):

        ref = Boolean()
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate('text', ref.schema())
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(0, ref.schema())

    def test_json(self):

        ref = Boolean()
        self.assertEqual('{"type": "boolean"}', text_type(ref))
