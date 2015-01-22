#!/bin/bash
# Publish these files.
# Assumes a virtualenv named HOMICIDE, as well as virtualenvwrapper.
# pip insall virtualenv; pip install virtualenvwrapper

workon HOMICIDE
CURRENT_YEAR=2015

for CITY in Denver "El Paso" Louisville Portland; do
    # Prep the variables
    echo $CITY

    # Lower-case city, replace spaces with hyphens
    slug=`echo $CITY | tr '[:upper:]' '[:lower:]' | tr ' ' '-'`
    echo $slug

    # Write the flat files
    python spreadsheet.py City="$CITY"

    # *** UPDATE AT THE START OF EACH YEAR
    for YEAR in 2014 2015; do
        python spreadsheet.py City="$CITY" Year=$YEAR
    done

    ls -lth output/*$slug*
done

# Output the whole year's spreadsheet
# *** UPDATE AT THE START OF EACH YEAR
for YEAR in 2014 2015; do
    python spreadsheet.py Year=$YEAR
done

./ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
