# -*- encoding: utf-8 -*-
"""
    flask_triangle.flask
    --------------------

    Addons provided to flask

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from jsonschema import validate, SchemaError, ValidationError
from flask import request, abort


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


def angular_filter(string):
    """A Jinja2 filter to generate double curly-bracketed string."""
    return u'{{{{{}}}}}'.format(string)
