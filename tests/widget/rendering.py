# -*- encoding: utf-8 -*-
"""
    flask-triangle.tests.widgets.rendering
    --------------------------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest, warnings, jinja2, bs4

from flask_triangle.widgets.standard import TextInput


def render(widget, template=None):

    if template is None:
        template = '''
            <html>
              <body>
                <form>
                  {{widget}}
                </form>
              </body>
            </html>
        '''

    return jinja2.Template(template).render(widget=widget)


def to_soup(html):
    with warnings.catch_warnings(record=True):
        return bs4.BeautifulSoup(html)


class TestRendering(unittest.TestCase):

    def setUp(self):

        self.widget = TextInput('bind', html_attributes={'custom': 'ok'})

    def test_rendered_as_safe_html(self):

        self.assertNotIn('&lt;', render(self.widget))

    def test_valid_html(self):

        soup = to_soup(render(self.widget))
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 1)

    def test_late_html_attribute(self):

        template = '''
            <html>
              <body>
                <form>
                  {{widget(class='test')}}
                </form>
              </body>
            </html>
        '''

        soup = to_soup(render(self.widget, template))
        inputs = soup.find_all('input', {'class': 'test'})
        self.assertEqual(len(inputs), 1)

    def test_overwrite_html_attribute(self):

        template = '''
            <html>
              <body>
                <form>
                  {{widget(custom='success')}}
                </form>
              </body>
            </html>
        '''

        soup = to_soup(render(self.widget, template))
        inputs = soup.find_all('input', {'custom': 'ok'})
        self.assertEqual(len(inputs), 0)
        inputs = soup.find_all('input', {'custom': 'success'})
        self.assertEqual(len(inputs), 1)
