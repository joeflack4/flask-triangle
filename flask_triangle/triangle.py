# -*- encoding: utf-8 -*-
"""
    flask_triangle.triangle
    -----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from .helpers import angular_filter


class Triangle(object):
    """
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.filters[u'angular'] = angular_filter
