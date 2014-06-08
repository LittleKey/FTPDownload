#!/usr/bin/env python
# encoding: utf-8

from FileList import FileTableFactory
from FTP import FTPFactory

def main():
    ftp = FTPFactory().GetFTP()
    factory = FileTableFactory(ftp)
    filetable = factory.New()

    print filetable.GetDirList()
    for l in factory.Listener:
        l.join()


if __name__ == "__main__":
    main()
