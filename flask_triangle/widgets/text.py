# -*- encoding: utf-8 -*-
"""

"""


from flask_triangle.widget import Widget


class TextInput(Widget):
    """A simple text input."""

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, index=0, **kwargs):

        super(TextInput, self).__init__(bind, name, validators, label,
                                        description, index, **kwargs)
        self.attributes[u'type'] = u'text'
