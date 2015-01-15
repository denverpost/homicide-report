#!/bin/bash
# Publish these files.

for CITY in Denver "El Paso"; do
    # Prep the variables
    echo $CITY

    # Lower-case city, replace spaces with hyphens
    slug=`echo $CITY | tr '[:upper:]' '[:lower:]' | tr ' ' '-'`
    echo $slug

    # Write the flat files
    python spreadsheet.py City="$CITY"
    ls -lth output/*$slug*
done
