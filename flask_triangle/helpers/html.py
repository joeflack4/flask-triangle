# -*- encoding: utf-8 -*-
'''

'''


from __future__ import absolute_import


class HTMLString(unicode):
    """An unicode overload for Jinja2."""
    def __html__(self):
        return self
