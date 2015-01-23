#!/bin/bash
# Publish these files.
# Assumes a virtualenv named HOMICIDE, as well as virtualenvwrapper.
# pip install virtualenv; pip install virtualenvwrapper
# Also assumes env vars REMOTE_DIR and REMOTE_HOST:
# export REMOTE_DIR='path/on/remote/server/to/publish'; export REMOTE_HOST='ftp.servername.com'

source /usr/local/bin/virtualenvwrapper.sh
workon HOMICIDE
CURRENT_YEAR=2015

for CITY in Denver "El Paso" Louisville Portland Nashville; do
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

# FTP the data files
./ftp.bash --dir $REMOTE_DIR/output --host $REMOTE_HOST
# FTP the static files (should only update them when necessary.)
./ftp.bash --dir $REMOTE_DIR --source_dir www --host $REMOTE_HOST
