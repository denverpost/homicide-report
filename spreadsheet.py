#!/usr/bin/env python
# Turn the spreadsheet into a flatfile.
import os
import sys
import json
import doctest
import gspread
from collections import defaultdict, OrderedDict
# from filewrapper import FileWrapper
from optparse import OptionParser


class Sheet:
    """ Handle google spreadsheet read and flatfile write operations.
        >>> sheet = Sheet('test-sheet', 'worksheet-name')
        >>> sheet.publish()
        True
        """

    def __init__(self, sheet_name, worksheet=None):
        # self.fw = FileWrapper()
        self.verbose = True
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir('%s/output' % self.directory):
            os.mkdir('%s/output' % self.directory)

        self.spread = gspread.login(os.environ.get('ACCOUNT_USER'), os.environ.get('ACCOUNT_KEY'))
        self.sheet_name = sheet_name
        if worksheet:
            self.open_worksheet(worksheet)
            self.worksheet = worksheet

    def slugify(self, slug):
        return slug.lower().replace(' ', '-')

    def open_worksheet(self, worksheet):
        """ Open a spreadsheet, return a sheet object.
            >>> sheet = Sheet('test-sheet')
            >>> sheet.open_worksheet('worksheet-name')
            <Worksheet 'worksheet-name' id:od6>
            """
        self.sheet = self.spread.open(self.sheet_name).worksheet(worksheet)
        return self.sheet

    def publish(self, worksheet=None):
        """ Publish the homicide data in whatever permutations we need.
            This assumes the spreadsheet's key names are in the first row.
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> sheet.publish()
            True
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        rows = self.sheet.get_all_values()
        keys = rows[0]
        fn = {
            'json': open('%s/output/%s.json' % (self.directory, worksheet), 'w'),
            'csv': open('%s/output/%s.csv' % (self.directory, worksheet), 'w')
        }
        for i, row in enumerate(rows):
            if i == 0:
                keys = row
                continue
            record = OrderedDict(zip(keys, row))
            # print record
            # *** Write to CSV & JSON files here. 
            # *** Also consider what filtering we may need to do based on fields in the dict.

        return True


def main():
    sheet = Sheet('Homicide Report', 'responses')
    sheet.publish()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    (options, args) = parser.parse_args()

    doctest.testmod(verbose=options.verbose)

    main()
