# -*- encoding: utf-8 -*-
"""
    flask_triangle.types
    --------------------

    This module implements custom types derivated for internal use.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


import collections


class Attributes(dict):
    """
    ``Attributes`` is a custom dict to hold pairs of key-values as attributes.

    An attribute with a `None` value will be considered as a boolean attribute
    but the others as standard attributes.
    """

    def __call__(self):
        """
        Returns a string containing every attributes, separated by spaces
        with the following grammar :

            * `key="value"` for standard attributes
            * `key` for boolean attributes
        """
        valued = u' '.join(u'{k}="{v}"'.format(k=k, v=v)
                           for k, v in self.items() if v is not None)

        boolean = u' '.join(u'{k}'.format(k=k) for k, v in self.items()
                            if v is None)

        return u' '.join((v for v in (valued, boolean) if v))


class Schema(dict):
    """
    ``Schema`` is a custom dict with a nesting update mechanism. If the
    the updated values of two fields are a dict or a list they're marged.
    Otherwhise, they are overwritten.
    """

    @staticmethod
    def __update(d, u):
        for k, v in u.iteritems():
            if isinstance(v, collections.Mapping):
                r = Schema.__update(d.get(k, {}), v)
                d[k] = r
            elif isinstance(v, list):
                r = d.get(k, [])
                d[k] = list(set(r + v))
            else:
                d[k] = u[k]
        return d

    def update(self, other):
        self.__update(self, other)
