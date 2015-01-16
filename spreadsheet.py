#!/usr/bin/env python
# Turn the spreadsheet into a flatfile.
import os
import sys
import json
import doctest
import csv
import gspread
from collections import defaultdict, OrderedDict
from optparse import OptionParser


class Sheet:
    """ Handle google spreadsheet read and flatfile write operations.
        >>> sheet = Sheet('test-sheet', 'worksheet-name')
        >>> sheet.publish()
        True
        """

    def __init__(self, sheet_name, worksheet=None):
        self.options = None
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir('%s/output' % self.directory):
            os.mkdir('%s/output' % self.directory)

        self.spread = gspread.login(
            os.environ.get('ACCOUNT_USER'),
            os.environ.get('ACCOUNT_KEY'))
        self.sheet_name = sheet_name
        self.filters = None
        if worksheet:
            self.open_worksheet(worksheet)
            self.worksheet = worksheet

    def set_options(self, options):
        """ Set the objects options var.
            """
        self.options = options
        return options

    def slugify(self, slug):
        return slug.lower().replace(' ', '-')

    def add_filter(self, key, value):
        """ Add a filter we will parse the spreadsheet by. Key should match
            a key in the spreadsheet (capitalization matters).
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> sheet.add_filter('name', 'test')
            True
            >>> sheet.filters
            [{'value': 'test', 'key': 'name'}]
            """
        if self.filters:
            self.filters.append({'key': key, 'value': value})
        else:
            self.filters = [{'key': key, 'value': value}]
        return True

    def build_filename(self):
        """ Put together the name of the file we're writing. This is based
            on the worksheet name and any filters.
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> sheet.add_filter('name', 'test')
            True
            >>> sheet.build_filename()
            True
            >>> sheet.filename
            'worksheet-name-test'
            """
        filter_string = ''
        if self.filters:
            filter_string += '-'
            for item in self.filters:
                filter_string += self.slugify(item['value'])

        self.filename = '%s%s' % (self.worksheet, filter_string)
        return True

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

        self.build_filename()

        rows = self.sheet.get_all_values()
        keys = rows[0]
        fn = {
            'json': open('%s/output/%s.json' % (self.directory, self.filename), 'wb'),
            'csv': open('%s/output/%s.csv' % (self.directory, self.filename), 'wb')
        }
        recordwriter = csv.writer(
            fn['csv'], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        records = []
        for i, row in enumerate(rows):
            if i == 0:
                keys = row
                recordwriter.writerow(keys)
                continue
            record = OrderedDict(zip(keys, row))

            publish = True
            if self.filters:
                for item in self.filters:
                    # Special handling for filtering by years. Hard-coded.
                    if record[item['key']] == 'Year':
                        if item['value'] not in record['Date of homicide']:
                            publish = False
                    elif record[item['key']] != item['value']:
                        publish = False

            if publish:
                if self.options and self.options.geocode:
                    if record['Latitude'] == '' or record['Longitude'] == '':
                        geo = Geocode('%s, %s' % (record['Address of homicide'], record['City']))
                        latlng = geo.get()
                        record['Latitude'] = latlng.split(',')[0]
                        record['Longitude'] = latlng.split(',')[1]
                        # *** Still need to write these values back to the spreadsheet
                recordwriter.writerow(row)
                records += [record]

        if records:
            json.dump(records, fn['json'])

        return True


def main(options, args):
    """ Take args as key=value pairs, pass them to the add_filter method.
        Example command:
        $ python spreadsheet.py City=Denver
        """
    sheet = Sheet('Homicide Report', 'responses')
    sheet.set_options(options)
    for arg in args:
        if '=' not in arg:
            continue
        k, v = arg.split('=')
        sheet.add_filter(k, v)
    sheet.publish()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-g", "--geocode", dest="geocode", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    (options, args) = parser.parse_args()

    if options.verbose:
        doctest.testmod(verbose=options.verbose)

    main(options, args)
