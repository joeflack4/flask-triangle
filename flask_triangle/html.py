# -*- encoding: utf-8 -*-
'''

'''


from __future__ import absolute_import


class HTMLString(unicode):

    def __html__(self):
        return self
