#!/usr/bin/env python3
# encoding: utf-8


import settings
from Select import Selector
from Subject import Subject
from time import sleep
from FTP import FTP
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class Listener(Subject, _threading.Thread):
    def __init__(self, ftp, fileListDir=settings.FTP_FileList_Dir):
        if not isinstance(ftp, FTP):
            raise TypeError

        #super(Listener, self).__init__()
        Subject.__init__(self)
        _threading.Thread.__init__(self)

        self._ftpFileListDir = fileListDir
        self._localFilelist = ''
        self._ftp = ftp

    def __GetList(self):
        return self._ftp.GetList(self._ftpFileListDir)

    def Listen(self, time=5*60):
        while self.HasElements():
            ftpFilelist = self.__GetList()
            if ftpFilelist != self._localFilelist:
                self._localFilelist = ftpFilelist
                #super(Listener, self).Notify(self._localFilelist)
                self.Notify(self._localFilelist)
                
            print("Wait 5 mins...")
            sleep(time)

    def run(self):
        self.Listen()

    @property
    def FtpFileListDir(self):
        return self._ftpFileListDir

    @FtpFileListDir.setter
    def FtpFileListDir(self, value):
        self._ftpFileListDir = value

    #@property
    #def FTP(self):
    #    return self._ftp

    #@FTP.setter
    #def FTP(self, value):
    #    if not isinstance(value, FTP):
    #        raise TypeError

    #    self._ftp = value
