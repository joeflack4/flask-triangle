# -*- encoding: utf-8 -*-
"""
    flask_triangle.helpers
    ----------------------

    Useful functions. Some of them are directly aimed to be available in Flask.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

import re
from flask import request, abort
from jsonschema import validate, SchemaError, ValidationError


def angular_attribute(name):
    """
    Translate an Angular's attribute name from camel case notation to dashed
    notation. Other name will not be modified::

    :arg name: An ``unicode`` string starting by 'ng[A-Z].*'.

        >>> angular_attribute(u'ngPattern')
        u'ng-pattern'
        >>> angular_attribute(u'other')
        u'other'
    """
    if not re.match(r'^ng[A-Z].*$', name):
        return name
    return u'-'.join(c for c in re.split(r'(^ng)|([A-Z][^A-Z]+)', name) if c).lower()


def angular_filter(string):
    """A Jinja2 filter to generate double curly-bracketed string."""
    return u'{{{{{}}}}}'.format(string)

#TODO: To test
def json_validate(schema):
    """
    A decorator to automatically handle JSON validation sent as payload.

    This decorator must be used on function triggered by a registered route
    in Flask. If the HTTP request is not valid it will raise an HTTP 415
    error. If the validation schema is not valid it will raise an HTTP 500
    error and finally, if the sent data is not valid an HTTP 400 error is
    raised.

    :arg schema: A json-schema dict to validate data against it.
    """
    def decorator(func):
        def wrapfunc(*args, **kwargs):
            if request.json is None:
                abort(415, u'Unsuported Media Type.'
                           u'Content-Type must by application/json')

            try:
                validate(request.json, schema)
            except SchemaError:
                abort(500)
            except ValidationError:
                abort(400, u'Bad Request. '
                           u'Sent JSON data is not valid.')
            return func(*args, **kwargs)
        return wrapfunc

    return decorator
