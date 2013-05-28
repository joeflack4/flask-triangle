'''
    Test the HTML rendering object
'''


from flask_triangle.html import HTMLString

from nose.tools import assert_true, assert_equal, assert_in


class TestHTMLString(object):

    def test_unicode(self):
        '''An HTMLString object is a unicode object.'''
        assert_true(issubclass(HTMLString, unicode))

    def test_html_method(self):
        '''An HTMLString as a special method __html__.'''
        assert_in('__html__', dir(HTMLString))

    def test_html_method_return(self):
        '''The html method returns the same as the unicode method.'''
        instance = HTMLString(u'test')
        assert_equal(instance.__html__(), unicode(instance))
