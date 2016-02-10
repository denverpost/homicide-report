#!/bin/bash
# Publish these files.
# Assumes a virtualenv named HOMICIDE, as well as virtualenvwrapper.
# pip install virtualenv; pip install virtualenvwrapper
# Also assumes env vars REMOTE_DIR and REMOTE_HOST:
# export REMOTE_DIR='path/on/remote/server/to/publish'; export REMOTE_HOST='ftp.servername.com'

source /usr/local/bin/virtualenvwrapper.sh
workon HOMICIDE
CURRENT_YEAR=2016
#declare -a CITIES=('Denver' '"El Paso"' 'Louisville' 'Portland' '"Portland Metro"' 'Nashville')
#declare -a METROS=('Portland')

for CITY in Denver Louisville Portland "Portland Metro" Nashville; do
    # Prep the variables
    echo $CITY

    # Lower-case city, replace spaces with hyphens
    slug=`echo $CITY | tr '[:upper:]' '[:lower:]' | tr ' ' '-'`
    echo $slug

    # Write the flat files
    python2.7 homicide.py City="$CITY"

    # *** UPDATE AT THE START OF EACH YEAR
    for YEAR in 2014 2015 2016; do
        python2.7 homicide.py City="$CITY" Year=$YEAR
    done

    ls -lth output/*$slug*
done

# Merge the json files for metro-area homicides
for METRO in portland; do
    cat output/responses-$METRO.json output/responses-$METRO-metro.json | sed 's/\]\[/,/g' > output/responses-$METRO-all.json
    echo "METRO: $METRO"
done

# Output the whole year's homicide
# *** UPDATE AT THE START OF EACH YEAR
for YEAR in 2014 2015 2016; do
    python2.7 homicide.py Year=$YEAR
done

# FTP the data files
./ftp.bash --dir $REMOTE_DIR/output --host $REMOTE_HOST
# FTP the static files (should only update them when necessary.)
./ftp.bash --dir $REMOTE_DIR --source_dir www --host $REMOTE_HOST
