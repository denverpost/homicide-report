#!/usr/bin/env python
import geocoder
from filewrapper import FileWrapper

class geocode:
    """ Lookup lat/lngs, and maintain cached geocode lookups.
        Returns two values (lat, lng) if available, False if not.
        >>> geo = geocode('Portland, OR')
        >>> lat, lng = geo.get()
        """

    def __init__(self, lookup):
        self.lookup = lookup

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
            return False, False
        try:
            g = geocoder.google(self.lookup)
            fh.write("%s,%s" % ( g.lat, g.lng ))
            return g.lat, g.lng
        except:
            return False, False
        return False, False
