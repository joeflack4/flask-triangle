'''
    Test the standard validator object
'''


from flask_triangle.validators import Required

from nose.tools import assert_in, assert_true, assert_false, assert_equal


class TestRequired(object):

    def setup(self):
        self.required = Required()
        self.angular = Required(u'0 == 1')

    def test_simple(self):
        '''Without initialization is_required is True'''
        assert_true(self.required.is_required())

    def test_simple_attr(self):
        '''Simple Required set the `required` attribute'''
        assert_in(u'required', self.required.attributes)

    def test_angular_required(self):
        '''An angular expression limit is_required to False'''
        assert_false(self.angular.is_required())

    def test_angular_attr(self):
        '''An angular expression set the `ng-required` attribute'''
        assert_in(u'ng-required', self.angular.attributes)
        assert_equal(self.angular.attributes.get(u'ng-required'), u'0 == 1')
