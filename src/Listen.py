#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
#import settings
#from Select import Selector
from Subject import Subject
from time import sleep
from FTP import FTP
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class Listener(_threading.Thread, Subject):
    def __init__(self, ftp, fileListDir, lock=_threading.Lock()):
        if not isinstance(ftp, FTP):
            raise TypeError

        #super(Listener, self).__init__()
        Subject.__init__(self)
        _threading.Thread.__init__(self)
        # 如果使用了多个Listener，并且他们都使用同一个lftp程序
        # 那么请使用同一个线程锁(lock)
        self.lock = lock
        # Notice filetype code in python3
        self.setName("{ftpHost}:{ftpDir}".format(ftpHost=ftp.host, ftpDir=fileListDir.encode("utf-8")))

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
                try:
                    self.Notify(self._localFilelist)
                except IOError:
                    exit()

            #print("[{ThreadName}]: Wait 5 mins...".format(ThreadName=self.getName()))
            sleep(time)

    def run(self):
        self.Listen()

    @property
    def FtpDir(self):
        return self._ftpFileListDir

    @FtpDir.setter
    def FtpDir(self, value):
        self._ftpFileListDir = value

    #@property
    #def FTP(self):
    #    return self._ftp

    #@FTP.setter
    #def FTP(self, value):
    #    if not isinstance(value, FTP):
    #        raise TypeError

    #    self._ftp = value
