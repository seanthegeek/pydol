#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""Unit tests for pydol

Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from os import environ
import unittest
import json

from pydol import DOLAPI


__author__ = "Sean Whalen"
__copyright__ = "Copyright (C) 2016 %s" % __author__
__license__ = "Apache 2.0"


class Test(unittest.TestCase):
    """Test suite for pydol"""

    # Ignore test method case
    # pylint: disable=C0103

    # Ignore number of methods
    # pylint: disable=R0904

    def setUp(self):
        """Creates instances for testing"""
        # Set standard values for testing
        self.dataset = "statistics/BLS_Numbers"
        self.table = "averageHourlyEarnings12MonthChange"
        self.table2 = "consumerPriceIndex12MonthChange"
        self.badstr = "blah"

        # Create authenticated and unauthenticated instances of DOLAPI
        self.unauth = DOLAPI()
        self.badauth = DOLAPI(self.badstr, self.badstr * 2)
        self.auth = DOLAPI(str(environ['DOL_KEY']), str(environ['DOL_SECRET']))

    def testMetadata(self):
        """Dataset metadata is accessible with and without API keys"""
        self.assertGreater(len(self.unauth.metadata(self.dataset)), 0)
        self.assertGreater(len(self.auth.metadata(self.dataset)), 0)

    def testMissingKeys(self):
        """Requesting table data without API credentials raises ValueError"""
        self.assertRaises(ValueError,
                          self.unauth.table,
                          self.dataset,
                          self.table)

    def testBadKeys(self):
        """Requesting table data with bad credentials raises _DOLAPIError"""
        # Ignore access to protected members
        # pylint: disable=W0212
        self.assertRaises(DOLAPI._DOLAPIError,
                          self.badauth.table,
                          self.dataset,
                          self.table)

    def testBadNames(self):
        """A bad dataset and/or or table name raises DOLAPI._DOLAPIError"""
        bad_dataset = self.badstr
        bad_table = self.badstr * 2
        # Ignore access to protected members
        # pylint: disable=W0212

        self.assertRaises(DOLAPI._DOLAPIError,
                          self.auth.table,
                          bad_dataset,
                          self.table)

        self.assertRaises(DOLAPI._DOLAPIError,
                          self.auth.table,
                          self.dataset,
                          bad_table)

        self.assertRaises(DOLAPI._DOLAPIError,
                          self.auth.table,
                          bad_dataset,
                          bad_table)

    def testTable(self):
        """Table retrieval succeeds without any options specified"""
        self.assertGreater(len(self.auth.table(self.dataset, self.table)), 0)

    def testMax(self):
        """The number of records returned does not exceed the top limit"""
        top = 10
        table = self.auth.table(self.dataset, self.table, top=top)
        record_count = len(table)
        self.assertLessEqual(record_count, top)

    def testSkip(self):
        """Record skipping"""
        skip = 1
        column = "year"
        skiped = self.auth.table(self.dataset, self.table, skip=skip, top=skip)
        unskiped = self.auth.table(self.dataset, self.table, top=skip)
        self.assertNotEqual(skiped[0][column], unskiped[0][column])

    def testFields(self):
        """API returns specific fields when requested"""
        requested_fields = ["year", "value"]
        table = self.auth.table(self.dataset,
                                self.table2,
                                fields=requested_fields)
        table_columns = table[0].keys()
        for x in requested_fields:
            self.assertTrue(x in table_columns)

        self.assertEqual(len(requested_fields), len(table_columns))

    def testOrderBy(self):
        """Request with order_by"""
        order_by = "year"
        table = self.auth.table(self.dataset,
                                self.table2,
                                order_by=order_by,
                                top=24)

        self.assertLess(table[0][order_by], table[23][order_by])
        order_by2 = "year desc"
        table = self.auth.table(self.dataset,
                                self.table2,
                                order_by=order_by2,
                                top=24)
        self.assertGreater(table[0][order_by], table[23][order_by])

    def testFilters(self):
        """Filtered requests"""
        filters = "type eq 'F'"
        table = self.auth.table(self.dataset, self.table2, filters=filters)
        self.assertGreater(len(table), 0)
        filters = "(type eq 'F') and (year eq 2013)"
        table = self.auth.table(self.dataset, self.table2, filters=filters)
        self.assertEqual(len(table), 12)

if __name__ == "__main__":
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
