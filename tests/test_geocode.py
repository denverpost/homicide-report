#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from geocode import Geocode

def test_setup():
    """ Can we even create an object?
        """
    g = Geocode('Portland, OR')
    assert g == True

def test_geocode():
    """ Test geocoding.
        """
    g = Geocode('Portland, OR')
    latlng = g.get()
    assert latlng == [45.5230622, -122.6764816]
