# -*- encoding: utf-8 -*-


from __future__ import absolute_import

from .html import HTMLString
from .types import Attributes, Schema
from .validators import Required
import re


class Widget(object):
    """
    The standard widget is a simple text input.
    """

    tag = u'input'
    as_json = u'string'
    as_html = u'text'

    def __init__(self, bind, name=None, id_=None, class_=None, validators=None,
                 legend=None, description=None, **kwargs):
        """
        :arg bind: An ``angular expression``. Two-way Angular's data binding
        using ngModel directive. See `Angular's ngModel directive` for more
        detail.

        .. _`Angular's ngModel directive`:
            http://docs.angularjs.org/api/ng.directive:ngModel

        :arg name: An ``unicode`` string. The name of the current widget in the
        generated HTML. This argument is optional but the property must be set
        in order to generate the HTML.

        :arg id_: An ``unicode`` string or an ``angular expression``. The id
        attribute of the current widget in the generated HTML.

        :arg class_: An ``unicode`` string or a ``list`` of unicode. The class
        attribute of the current widget. If the argument is a list, all classes
        will be space separated.

        :arg validators: A ``list`` of ``Validator`` instances. A list of
        validation taks applied to the value of the widget. Each validation can
        be client-side, server-side or both. See ``Validators`` in this
        documentation for more details.

        :arg legend: A ``unicode`` string or an ``angular expression``. An
        optional legend for the current widget.

        :arg description: A ``unicode`` string or an ``angular expression``. An
        optional description for current widget.

        :arg kwargs: Each keyword arguments will be considered as attributes
        of the HTML rendered widget. The argument starting with "ng[A-Z].*"
        will be converted from camelCase to a dashed version of them to comply
        with the Angular's API. See `Angular's API` for more detail.

        .. _`Angular's API`:
            http://docs.angularjs.org/api/
        """

        self.legend = legend
        self.description = description
        self.validators = validators if validators is not None else []

        self.attributes = Attributes({u'name': name,
                                      u'type': self.as_html,
                                      u'ng-model': bind})

        if id_ is not None:
            self.attributes[u'id'] = id_

        if class_ is not None:
            if type(class_) in (list, set, tuple):
                self.attributes[u'class'] = ' '.join(class_)
            else:
                self.attributes[u'class'] = class_

        for k, v in kwargs.items():
            if re.match(r'^ng[A-Z].*$', k):
                k = u'-'.join((item for item in re.split(r'([A-Z][^A-Z]+)', k)
                               if item)).lower()
            self.attributes[k] = v

    # name is a special attribute also acting as a property.
    @property
    def name(self):
        return self.attributes[u'name']

    @name.setter
    def name(self, value):
        self.attributes[u'name'] = value

    @property
    def schema(self):
        """
        Returns a json-schema dict to validate this specific widget.
        """
        levels = self.attributes.get(u'ng-model').split(u'.')
        # required is a special validator not directly affecting the current
        # properties but all it's nesting chain.
        required = any(val.is_required() for val in self.validators
                       if type(val) is Required)

        root = Schema({u'type': u'object', u'properties': {}})

        parent = root
        for child in levels[:-1]:
            new = {child: {u'type': u'object', u'properties': {}}}
            parent.get(u'properties').update(new)
            if required:
                parent.update({u'required': [child]})
            parent = new.get(child)

        parent.get(u'properties').update({levels[-1]: {u'type': self.as_json}})
        if required:
            parent.update({u'required': [levels[-1]]})

        return root

    def html(self):
        """
        Returns the valid HTML for the current widget.
        """
        if self.name is None:
            raise ValueError(u'The required `name` property is not set.')
        if self.attributes.get(u'ng-model', None) is None:
            raise ValueError(u'The field is unbound.')

        return u'<{tag} {attr}/>'.format(tag=self.tag, attr=self.attributes())

    def __call__(self, **kwargs):
        """
        Call to format the HTML string.
        """
        return HTMLString(self.html().format(**kwargs))
