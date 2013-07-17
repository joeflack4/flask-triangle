# -*- encoding: utf-8 -*-
"""
    widgets.advanced.datepicker
    ---------------------------

    /!\ UNTESTED /!\

    An experimental datepicker widget based on `ui.bootstrap.datepicker`
    and inspired by bootstrap-datepicker.js.

    This widget depends on 'triangle.datepicker' in your triangle
    application. (see: https://gist.github.com/morgan-del/6021530)

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

from ..base import Widget, HtmlAttr


class Datepicker(Widget):

    html_template = '''
    <div class="btn-group">
      <input {attributes}>
      <div class="dropdown-menu persistent-dropdown">
        <datepicker {datepicker_attributes}></datepicker>
      </div>
    </div>
    '''
    json_type = 'text'

    def __init__(self, bind, name=None, validators=None, label=None,
                 description=None, starting_day=1, date_min=None,
                 date_max=None, date_format='yyyy-MM-dd'):

        self.datepicker_attributes = HtmlAttr({'starting-day': starting_day,
                                               'ng-model': bind})

        if date_min is not None:
            self.datepicker_attributes['min'] = date_min
        if date_max is not None:
            self.datepicker_attributes['max'] = date_max

        super(Datepicker, self).__init__(bind, name, validators, label,
                                         description,
                                         {'class': 'dropdown-toggle',
                                          'data-toggle': 'dropdown',
                                          'type': 'text'})

        del self.attributes['ng-model']
        self.attributes['value'] = '{}|date:\'{}\'|angular'.format(bind,
                                                                   date_format)

    def render(self):
        return self.html_template.format(attributes=self.attributes,
                                         datepicker_attributes = self.datepicker_attributes)
