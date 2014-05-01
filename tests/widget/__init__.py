# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from .customize import (
    TestCustomize,
    TestCustomizeInheritance,
    TestCustomizePriority
)

from .rendering import (
    TestRendering,
)

from .base import (
    TestBaseWidget,
)

__all__ = [
    'TestRendering',
    'TestCustomize',
    'TestCustomizeInheritance',
    'TestCustomizePriority',
    'TestBaseWidget'
]
