# -*- encoding: utf-8 -*-
"""
    test.schema.container
    ---------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from .base import SanityCheck, CheckBaseProperties, CheckCacheMechanism
from .container import CheckContainerProperties, CheckDataValidation, \
                       CheckMerging, CheckPropertyAccess
from flask_triangle.schema import Object


class TestSchema(SanityCheck, CheckBaseProperties, CheckCacheMechanism):
    """
    Execute all the base tests.
    """
    def setup(self):
        self.item = Object()


class TestSchemaContainerProperties(CheckContainerProperties,
                                    CheckDataValidation,
                                    CheckPropertyAccess):
    """
    Test the common properties of the containers.
    """
    def setup(self):
        self.item = Object()


class TestObjectMerging(CheckMerging):
    """
    Test the common properties of the containers.
    """
    def setup(self):
        self.a = Object()
        self.b = Object()