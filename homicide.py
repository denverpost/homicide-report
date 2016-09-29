#!/usr/bin/env python
"""homicide.py docstring
Turn the homicide spreadsheet into a flatfile.
"""
import os
import sys
import json
import doctest
import csv
import codecs, cStringIO
import datetime, time
from docopt import docopt
import gspread
from spreadsheet import Sheet
from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
from optparse import OptionParser


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Homicide:
    """ Handle the homicide spreadsheet-specific parts of publishing
        from Google Sheets.
        >>> sheet = Sheet('test-sheet', 'worksheet-name')
        >>> homicide = Homicide(sheet)
        """
    def __init__(self, sheet):
        self.sheet = sheet
        self.is_metro = False

    def publish(self, worksheet=None):
        """ Publish the homicide data in whatever permutations we need.
            This assumes the spreadsheet's key names are in the first row.
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> homicide = Homicide(sheet)
            >>> homicide.publish()
            True
            """
        if not self.sheet.sheet or worksheet:
            self.sheet.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.sheet.worksheet

        self.sheet.build_filename()

        rows = self.sheet.sheet.get_all_values()
        keys = rows[0]
        fn = {
            'json': open('%s/output/%s.json' % (self.sheet.directory, self.sheet.filename), 'wb'),
            'jsonp': open('%s/output/%s.jsonp' % (self.sheet.directory, self.sheet.filename), 'wb'),
            'csv': open('%s/output/%s.csv' % (self.sheet.directory, self.sheet.filename), 'wb')
        }
        recordwriter = UnicodeWriter(fn['csv'], delimiter=',', 
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
        records = []
        for i, row in enumerate(rows):
            if i == 0:
                keys = row
                recordwriter.writerow(keys)
                continue
            record = OrderedDict(zip(keys, row))

            # We write lines one-by-one. If we have filters, we run
            # through them here to see if we're handling a record we
            # shouldn't be writing.
            publish = True
            if self.sheet.filters:
                for item in self.sheet.filters:
                    # Special handling for filtering by years. Hard-coded.
                    if item['key'] == 'Year':
                        if item['value'] not in record['Date of homicide']:
                            publish = False
                    elif record[item['key']] != item['value']:
                        publish = False

            if publish:
                if self.sheet.options and self.sheet.options.geocode:
                    if record['Latitude'] == '' or record['Longitude'] == '':
                        geo = Geocode('%s, %s' % (record['Address of homicide'], record['City']))
                        latlng = geo.get()
                        record['Latitude'] = latlng.split(',')[0]
                        record['Longitude'] = latlng.split(',')[1]
                        # *** Still need to write these values back to the spreadsheet
                if self.is_metro:
                    record['is_metro'] = 1

                # Turn the date into a timestamp.
                try:
                    record['unixtime'] = int(time.mktime(
                                                         datetime.datetime.strptime(record['Date of homicide'],
                                                         "%m/%d/%Y").timetuple()))
                except:
                    record['unixtime'] = 0
                
                recordwriter.writerow(row)
                records += [record]

        if records:
            json.dump(records, fn['json'])
            content = json.dumps(records)
            fn['jsonp'].write('homicide_callback(%s);' % content)

        return True

def main(options, args):
    """ Take args as key=value pairs, pass them to the add_filter method.
        Example command:
        $ python homicide.py City=Denver
        or
        $ python homicide.py City="Portland Metro"
        """
    sheet = Sheet('Homicide Report', 'responses')
    sheet.set_options(options)
    is_metro = False
    for arg in args:
        if '=' not in arg:
            continue
        k, v = arg.split('=')

        # Metro-specific special case
        if k.lower() == 'city' and 'etro' in v:
            is_metro = True
        sheet.add_filter(k, v)
    homicides = Homicide(sheet)
    homicides.is_metro = is_metro
    homicides.publish()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-g", "--geocode", dest="geocode", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    #parser.add_option("-h", "--help", dest="help", default=False, action="store_true")
    (options, args) = parser.parse_args()

    if options.verbose:
        doctest.testmod(verbose=options.verbose)
    '''
    if 'help' in options:
        print """
Downloads, filters and re-publishes the Google sheet of homicides.
Takes arguments based on the field names in the sheet.

Example command:
$ python homicide.py City=Denver
or
$ python homicide.py City="Portland Metro"
        """
    '''

    main(options, args)
