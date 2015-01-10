#!/usr/bin/env python
# Turn the spreadsheet into a flatfile.
import os
import sys
import json
import gspread
#from filewrapper import FileWrapper
from optparse import OptionParser

class Sheet:
    """ Handle google spreadsheet read and flatfile write operations.
        >>> sheet = Sheet()
        >>> sheet.read()
        """

    def __init__(self):
        #self.fw = FileWrapper()
        self.verbose = True
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.spread = gspread.login(os.environ.get('ACCOUNT_USER'), os.environ.get('ACCOUNT_KEY'))

    def slugify(self, slug):
        return slug.lower().replace(' ', '-')

    def publish(self, worksheet, options):
        """ Publish the homicide data in whatever permutations we need.
            >>> sheet = Sheet()
            """
        sheet = self.spread.open('homicides').worksheet('homicides')
        rows = sheet.get_all_values()
        keys = rows[0]
        fn = { 
            json: open('%s/output/%s.json' % (self.directory, worksheet), 'w'),
            csv: open('%s/output/%s.csv' % (self.directory, worksheet), 'w')
        }
        for i, row in enumerate(rows):
            if i == 0:
                keys = row
                continue
            

def main():
    pass

if __name__ == '__main__':
    main()
