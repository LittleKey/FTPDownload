#!/usr/bin/env python
# encoding: utf-8

from FTP import FTPFactory
import sys
from Downloader import NewDownload

def main(sysList):
    ftp = FTPFactory().GetFTP()
    NewDownload(ftp, *sysList)

if __name__ == "__main__":
    main(sys.argv[1:])
