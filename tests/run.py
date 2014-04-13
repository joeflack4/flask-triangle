# -*- encoding: utf-8 -*-
"""
    tests
    -----

    Entry-point of the testsuite.

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import with_statement
from __future__ import absolute_import
from __future__ import unicode_literals


# testenv setup

import os
import sys
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# import all the tests here

from helpers import *


if __name__ == '__main__':

    unittest.main()
