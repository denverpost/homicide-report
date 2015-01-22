#!/bin/bash
# ftp files from one directory to another.
# Assumes credentials are stored in a file in the home directory named .ftppass
# Variables can be set in the environment, or by command line argument
#
#
# NOTE: FTP IS AN INSECURE PROTOCOL AND SHOULD BE AVOIDED.

SOURCEDIR=''
DIR=''
HOST=''
USER=''
PASS=`cat ~/.ftp_pass`
FILES='*'
while [ "$1" != "" ]; do
    case $1 in
        -d | --dir ) shift
            DIR=$1
            ;;
        -h | --host ) shift
            HOST=$1
            ;;
        -u | --user ) shift
            USER=$1
            ;;
        -f | --files ) shift
            FILES=$1
            ;;
    esac
    shift
done

cd $SOURCEDIR
ftp -v -n $HOST << EOF
user $USER $PASS
cd $DIR
bin
passive
prompt
mput $FILES
bye                                                                                                                                                                          
EOF

#for FILE in `ls *.html`; do echo "mput $FILE"; done

