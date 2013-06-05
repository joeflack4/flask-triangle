# -*- encoding: utf-8 -*-
"""
    flask_triangle.triangle
    -----------------------

    This module provides the base tools of Flas-triangle.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from flask import request, abort
from jsonschema import validate, SchemaError, ValidationError


class Triangle(object):
    """
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.filters[u'angular'] = angular_filter


def angular_filter(string):
    """A Jinja2 filter to generate double curly-bracketed string."""
    return u'{{{{{}}}}}'.format(string)


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
                abort(400, u'Bad Request.'
                           u'Sent JSON data is not valid.')
            return func(*args, **kwargs)
        return wrapfunc

    return decorator
