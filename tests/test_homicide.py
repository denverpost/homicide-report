#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from spreadsheet import Sheet
from homicide import Homicide

def test_publish():
    """ Test the Sheet's publish method.
        """
    sheet = Sheet('test-sheet', 'worksheet-name')
    homicide = Homicide(sheet)
    publish_value = homicide.publish()
    assert publish_value == True
