#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from spreadsheet import Sheet

def test_publish():
    """ Test the Sheet's publish method.
        """
    sheet = Sheet('test-sheet', 'worksheet-name')
    sheet.publish()
