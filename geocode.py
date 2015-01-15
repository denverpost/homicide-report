#!/usr/bin/env python
import os
import geocoder
import slugify
from filewrapper import FileWrapper

class Geocode:
    """ Lookup lat/lngs, and maintain cached geocode lookups.
        Returns a list with two values (lat, lng) if available, False if not.
        >>> geo = Geocode('Portland, OR')
        >>> print geo.get()
        [45.5230622, -122.6764816]
        """

    def __init__(self, lookup):
        self.lookup = lookup
        if not os.path.isdir('geocode'):
            os.mkdir('geocode')

    def __self__(self):
        return self.lookup

    def set_lookup(self, lookup):
        """ Update the lookup value.
            """
        self.lookup = lookup
        return lookup

    def parse_lookup(self):
        """ Does some basic parsing on the geo lookup.
            """
        replacements = {
            'co': 'Colorado',
            'mn': 'Minnesota',
            'az': 'Arizona',
            'in': 'Indianapolis'
        }
        for key, value in replacements:
            if self.lookup[-2:].lower() == key:
                self.lookup = "%s%s" % (self.lookup[:-2], value)

    def get(self):
        """ See if a cached value for this lookup exists. If not, look it up.
            """
        self.parse_lookup()
        # Convert the lookup string into something suitable for a filename.
        fh = FileWrapper('geocode/%s.csv' % slugify.slugify(u'%s' % self.lookup))
        if fh.exists():
            geo_parts = fh.read()
            if "," in geo_parts:
                return geo_parts.split(',')
            return False
        try:
            g = geocoder.google(self.lookup)
            fh.write("%s,%s" % ( g.lat, g.lng ))
            return [g.lat, g.lng]
        except:
            return False
        return False
