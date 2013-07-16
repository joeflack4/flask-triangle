# -*- encoding: utf-8 -*-
"""
    template
    --------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import

from .attributes import TestAttributes0, TestAttributes1
from .widget import TestWidgetValidator, TestWidgetSchema,\
                    TestWidgetProperties, TestWidgetInit
from .core import TestTextInput, TestPasswordInput, TestEmailInput,\
                  TestCheckboxInput, TestRadioInput, TestRadioGroupInput

__all__ = ['TestAttributes0', 'TestAttributes1', 'TestWidgetValidator',
           'TestWidgetSchema', 'TestWidgetProperties', 'TestWidgetInit',
           'TestTextInput', 'TestPasswordInput', 'TestEmailInput',
           'TestCheckboxInput', 'TestRadioInput', 'TestRadioGroupInput']
