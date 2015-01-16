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

# *** FTP the files here
