# -*- encoding: utf-8 -*-
"""
"""


class Modifier(object):
    """
    The Modifier implements three methods to alter a widget entirely, its HTML
    attributes or its schema.

    This is the base class of every Modifiers.
    """

    def alter_widget(self, widget):
        """
        Modify the widget.

        :param widget: A :class:`Widget` instance.
        """
        pass

    def alter_html_attr(self, html_attrs):
        """
        Modify the HTML attributes.

        :param html_attrs: A `dict` instance holding the HTML attributes.
        """
        pass

    def alter_schema(self, schema, bind):
        """
        Modify the content of the `Schema` instance.

        :param schema: A :class:`Schema` instance.
        :param bind: A string of the Fully Qualified Name of the value bound
                     with the widget.

        The presence of the FQN acts as an accelerator for the schema
        manipulations rather than parse all of its content.
        """
        pass
