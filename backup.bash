#!/bin/bash
# Backup the spreadsheet if changes have been made to it.
# Assumes a virtualenv named HOMICIDE, as well as virtualenvwrapper.
# pip install virtualenv; pip install virtualenvwrapper

source source.bash # If it exists
source /usr/local/bin/virtualenvwrapper.sh
workon HOMICIDE
CURRENT_YEAR=2016

cp output/responses.csv output/current.csv
python homicide.py
DIFF=`diff output/responses.csv output/current.csv`

# If there was a difference, save the new spreadsheet in the backup dir.
if [ ! -z "$DIFF" ]; then 
    mkdir backup
    cp output/responses.csv backup/`date +'%F-%H'`.csv
fi

rm output/current.csv
