#!/usr/bin/env python
# Turn the spreadsheet into a flatfile.
import os
import sys
import json
import gspread
# from filewrapper import FileWrapper
from optparse import OptionParser


class Sheet:
    """ Handle google spreadsheet read and flatfile write operations.
        >>> sheet = Sheet('test-sheet', 'worksheet-name')
        >>> sheet.publish()
        """

    def __init__(self, sheet_name, worksheet=None):
        # self.fw = FileWrapper()
        self.verbose = True
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.spread = gspread.login(os.environ.get('ACCOUNT_USER'), os.environ.get('ACCOUNT_KEY'))
        self.sheet_name = sheet_name
        if worksheet:
            self.open_sheet(worksheet)
            self.worksheet = worksheet

    def slugify(self, slug):
        return slug.lower().replace(' ', '-')

    def open_worksheet(self, worksheet, options=None):
        """ Open a spreadsheet, return a sheet object.
            >>> sheet = Sheet('test-sheet')
            >>> sheet.open_worksheet('worksheet-name')
            """
        self.sheet = self.spread.open(self.sheet_name).worksheet(worksheet)
        return self.sheet

    def publish(self, worksheet=None):
        """ Publish the homicide data in whatever permutations we need.
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
            record = dict(zip(keys, row))
            print record

        return True


def main():
    sheet = Sheet()
    sheet.publish('Homicide Report', 'responses')

if __name__ == '__main__':
    main()
