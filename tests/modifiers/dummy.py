# -*- encoding: utf-8 -*-
"""
    flask_triangle.tests.modifiers.dummy
    ------------------------------------

    Provide a dummy widget for testing.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from flask_triangle.widgets.widget import Widget
from flask_triangle.schema import String


class DummyWidget(Widget):

    atomic_schema = String()
    html_template = (
        '<div class="test">'
        '  <span{% if attrs %} {{attrs}}{% endif %}></span>'
        '</div>'
    )
