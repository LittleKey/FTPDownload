#!/usr/bin/env python
# encoding: utf-8

from FileList import FileTableFactory
from FTP import FTPFactory
import time

def main():
    ftp = FTPFactory().GetFTP()
    factory = FileTableFactory(ftp)
    filetable = factory.New()

    while True:
        time.sleep(10)
        print(filetable.GetFileList())

    for l in factory.Listener:
        l.join()


if __name__ == "__main__":
    main()
