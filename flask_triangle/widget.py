# -*- encoding: utf-8 -*-


from __future__ import absolute_import

from .html import HTMLString
from .types import Attributes, Schema
from .validators import Properties
import re


class Widget(object):
    """
    The standard widget is a simple text input.
    """

    tag = u'input'
    as_json = u'string'
    as_html = u'text'

    def __init__(self, bind, name=None, id_=None, class_=None, validators=None,
                 label=None, description=None, **kwargs):
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

        :arg label: A ``unicode`` string or an ``angular expression``. An
        optional label for the current widget.

        :arg description: A ``unicode`` string or an ``angular expression``. An
        optional description for current widget.

        :arg kwargs: Each keyword arguments will be considered as attributes
        of the HTML rendered widget. The argument starting with "ng[A-Z].*"
        will be converted from camelCase to a dashed version of them to comply
        with the Angular's API. See `Angular's API` for more detail.

        .. _`Angular's API`:
            http://docs.angularjs.org/api/
        """

        self._schema = None
        self._label = label
        self.description = description

        self.validators = [Properties(bind, self.as_json)]
        if validators is not None:
            self.validators += validators

        self.attributes = Attributes({u'name': name,
                                      u'type': self.as_html,
                                      u'ng-model': bind})

        # manage attributes
        if id_ is not None:
            self.attributes[u'id'] = id_

        if class_ is not None:
            if type(class_) in (list, set, tuple):
                self.attributes[u'class'] = ' '.join(class_)
            else:
                self.attributes[u'class'] = class_

        for validator in self.validators:
            self.attributes.update(validator.attributes())

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
    def label(self):
        if self._label is None:
            return self.name
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def schema(self):
        """
        Lazy loading of the schema.
        """
        if self._schema is None:
            self._schema = self.build_schema()

        return self._schema

    #TODO: Test this !
    def build_schema(self):
        """
        Builds the json-schema of a widget.

        The json-schema skeleton is built by the ``Properties`` validator. Each
        other validators will alter this skeleton by adding new properties.
        This method is quite complex ( On*m where n is the depth of the json
        binding an m the number of validators - at least one - ).
        """
        # The validation schema is built from the validators.

        levels = self.attributes[u'ng-model'].split(u'.')

        res = Schema()

        for validator in self.validators:

            root, nodes, leaf = validator.alter_schema

            current = res
            for i, node in enumerate(levels):
                if node == levels[0] and root:
                    current.update(validator.schema(child=node, name=None))
                current = current.get(u'properties').get(node)
                if current is None:
                    break
                if node != levels[-1] and nodes:
                    current.update(validator.schema(child=levels[i+1],
                                                    name=node))
                if node == levels[-1] and leaf:
                    current.update(validator.schema(child=None, name=node))

        return res

    def __call__(self, **kwargs):
        """
        Call to format the HTML string.
        """
        if self.name is None:
            raise ValueError(u'The required `name` property is not set.')
        res = u'<{tag} {attr}/>'.format(tag=self.tag, attr=self.attributes())
        return HTMLString(res.format(**kwargs))
