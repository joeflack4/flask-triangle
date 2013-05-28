'''
    Test validation
'''


from flask_triangle.widgets import TextInput
from flask_triangle.validators import Required
from jsonschema import validate, ValidationError

from nose.tools import raises


class TestRequired(object):
    """
    Impact of the required field on the validation process
    """

    def setup(self):
        self.not_required = TextInput(u'val', name='test')
        self.required = TextInput(u'val', name='test', validators=[Required()])

    def test_ok0(self):
        """unrequired value is present"""
        validate({u'val': 'ok'}, self.not_required.schema)

    def test_ok1(self):
        """required value is present"""
        validate({u'val': 'ok'}, self.required.schema)

    def test_missing0(self):
        """unrequired value is missing"""
        validate({}, self.not_required.schema)

    @raises(ValidationError)
    def test_missing1(self):
        """required value is missing raises an exception"""
        validate({}, self.required.schema)
