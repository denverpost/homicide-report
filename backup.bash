#!/bin/bash
# Backup the spreadsheet if changes have been made to it.
# Assumes a virtualenv named HOMICIDE, as well as virtualenvwrapper.
# pip install virtualenv; pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
workon HOMICIDE
CURRENT_YEAR=2015

cp output/responses.csv output/current.csv
python homicide.py
DIFF=`diff output/responses.csv output/current.csv`
