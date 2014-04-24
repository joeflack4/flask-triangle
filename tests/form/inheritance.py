# -*- encoding: utf-8 -*-
"""
    tests.form.inheritance
    ----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals

import unittest, warnings, bs4

from flask_triangle import Form
from flask_triangle.widgets.standard import TextInput


class TestForm(Form):

    field0 = TextInput('a.widget')

class TestForm1(TestForm):

    field0 = TextInput('a.widget.override')

class TestForm2(TestForm):

    field1 = TextInput('a.different.widget')

class TestForm3(TestForm1):

    field1 = TextInput('a.different.widget')

class TestForm4(TestForm1):

    field0 = None
    field1 = TextInput('a.different.widget')

class TestForm5(TestForm1):

    field0 = None


def to_soup(form):
    resp = '<form>{}</form>'.format(''.join(str(f) for f in form))
    with warnings.catch_warnings(record=True):
        return bs4.BeautifulSoup(resp)


class TestHTML(unittest.TestCase):

    def test_0(self):
        soup = to_soup(TestForm())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 1)
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.widget',
                                                  'name': 'field0'}))

    def test_1(self):
        soup = to_soup(TestForm1())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 1)
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.widget.override',
                                                  'name': 'field0'}))
        self.assertFalse(soup.find('input', attrs={'ng-model': 'a.widget',
                                                   'name': 'field0'}))

    def test_2(self):
        soup = to_soup(TestForm2())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 2)
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.widget',
                                                  'name': 'field0'}))
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.different.widget',
                                                  'name': 'field1'}))

    def test_3(self):
        soup = to_soup(TestForm3())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 2)
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.widget.override',
                                                  'name': 'field0'}))
        self.assertFalse(soup.find('input', attrs={'ng-model': 'a.widget',
                                                   'name': 'field0'}))
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.different.widget',
                                                  'name': 'field1'}))

    def test_4(self):
        soup = to_soup(TestForm4())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 1)
        self.assertFalse(soup.find('input', attrs={'ng-model': 'a.widget',
                                                  'name': 'field0'}))
        self.assertTrue(soup.find('input', attrs={'ng-model': 'a.different.widget',
                                                  'name': 'field1'}))

    def test_5(self):
        soup = to_soup(TestForm5())
        inputs = soup.find_all('input')
        self.assertEqual(len(inputs), 0)
