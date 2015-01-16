#!/usr/bin/env python
# FTP files with python.
from ftplib import FTP
import os
from optparse import OptionParser

class FtpWrapper():
    """ class ftpWrapper handles FTP operations. Assumes the password is stored
        in a file named '.ftppass' in the class directory.
        Currently this works best for uploading one or two files. Needs to be
        built out if it's going to handle large numbers of file uploads.
        """

    def __init__(self, user, host, upload_dir, pass_path='.ftppass', port=21):
        self.user = user
        self.host = host
        self.upload_dir = upload_dir

        file_h = open(pass_path, 'r')
        self.password = file_h.read()
        file_h.close

        self.port = port
        self.options = None

    def set_options(self, options):
        """ Set the object's options value.
            """
        self.options = options
        return options

    def ftp_callback(self, data):
        if self.options.verbose:
            print
            print
            print
            print data

    def ftp_file(self, fn):
        """ Open a connection, read a file, upload that file.
            Requires the filename.
            """
        file_h = open(fn, 'r')
        #blocksize = len(file_h.read())
        #print file_h.read()
        blocksize = 4096
        ftp = FTP(self.host, self.user, self.password)
        ftp.cwd(self.upload_dir)
        try:
            ftp.storbinary('STOR %s' % fn, file_h, blocksize, self.ftp_callback)
            print 'SUCCESS: FTP\'d %s to %s' % (fn, self.host)
        except:
            print 'ERROR: Could not FTP-->STOR %s' % fn
        file_h.close

if __name__ == '__main__':
    # Example call:
    # python FtpWrapper.py --user me --host them --filename it.html --path /put/it/there
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    parser.add_option("-o", "--host", dest="host", default='')
    parser.add_option("-u", "--user", dest="user", default='')
    parser.add_option("-f", "--filename", dest="filename", default='')
    parser.add_option("-p", "--path", dest="path", default='')
    (options, args) = parser.parse_args()
    ftz = FtpWrapper(options.user, options.host, options.path)
    ftz.ftp_file(options.filename)
