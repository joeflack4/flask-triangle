# -*- encoding: utf-8 -*-


import re
from flask_triangle.widget import Widget
from flask_triangle.validators import Required
from jsonschema import validate

from nose.tools import raises, assert_true, assert_in, assert_not_in, \
                       assert_equal


class TestWidget(object):

    def setup(self):
        self.widget = Widget(u'bound', u'name', custom=u'test', boolean=None)

    def test_bound(self):
        """
        An widget field must have a bound value stored in its 'ng-model'
        attribute.
        """
        assert_in(u'ng-model="bound"', self.widget.attributes())

    def test_name(self):
        """An widget field must have a name stored in its attributes."""
        assert_in(u'name="name"', self.widget.attributes())

    def test_name_property(self):
        """The name can be accessed as a distinct property."""
        assert_equal(self.widget.name, u'name')

    def test_name_setproperty(self):
        """The name can be set as a distinct property."""
        self.widget.name = u'test'
        assert_in(u'name="test"', self.widget.attributes())

    def test_kwargs(self):
        """Additional keyword arguments are treated as custom parameters."""
        assert_in(u'custom="test"', self.widget.attributes())

    def test_boolean_attributes(self):
        """
        Additionnal keyword arguments set to None are considered as boolean
        attributes.
        """
        assert_in(u'boolean', self.widget.attributes())
        assert_not_in(u'boolean=', self.widget.attributes())

    def test_angular_directives(self):
        """
        AngularJS directives start with 'ng' and are converted from ngCamelCase
        to ng-camel-case.
        """
        test = Widget(u'bound', u'name', ngClassEven='\'even\'')
        assert_in(u'ng-class-even="\'even\'"', test.attributes())

    def test_id_attributes(self):
        """id_ is a special parameter to set the id attribute."""
        test = Widget(u'bound', u'name', id_=u'test')
        assert_in(u'id="test"', test.attributes())

    def test_class_attributes(self):
        """class_ is a special parameter to set the class attribute."""
        test = Widget(u'bound', u'name', class_=u'test')
        assert_in(u'class="test"', test.attributes())

    def test_class_list_attributes(self):
        """
        class_ is a special parameter to set the class attribute. If the
        given parameter is a list of value, it is concatenated as a simple
        space separated string.
        """
        test = Widget(u'bound', u'name', class_=[u'test0', u'test1'])
        assert_in(u'class="test0 test1"', test.attributes())

    @raises(ValueError)
    def test_unbound(self):
        """
        An unbound widget field will raise a ValueError when HTML is rendered.
        """
        test = Widget(None, u'name')
        test()

    @raises(ValueError)
    def test_unamed(self):
        """
        An widget must have a name attribute or it will raise a ValueError when
        HTML is rendered.
        """
        test = Widget(u'bound')
        test()

    def test_html_simple_rendering(self):
        """
        An widget render valid HTML with all its attributes set when called.
        """
        assert_true(re.match(r'<("[^"]*"|\'[^\']*\'|[^\'">])*>', self.widget()))
        assert_in(self.widget.attributes(), self.widget())

    def test_html_formatable_rendering(self):
        """
        The resulting HTML can be formated if it conforms to python string
        format techniques and keyword arguments are passed when calling it.
        """
        test = Widget(u'bound', u'name', param='{test}')
        assert_not_in(u'param="{test}"', test(test=u'success'))
        assert_in(u'param="success"', test(test=u'success'))

    def test_json_schema(self):
        """The resulting dict for json-schema validation is valid."""
        validate({}, self.widget.schema)

    def test_json_schema_nesting(self):
        """
        The resulting dict for json-schema validation is valid when the bound
        to a nested object
        """
        test = Widget(u'this.is.nested.bound', u'name', param='{test}')
        validate({}, test.schema)

    def test_json_scema_required(self):
        """
        When the field is required, a required options appears as a list
        containing the current field name in the schema.
        """
        test = Widget(u'field', u'name', validators=[Required()])
        assert_in(u'required', test.schema)
        assert_in(u'field', test.schema.get(u'required', []))
