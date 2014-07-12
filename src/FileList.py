#!/usr/bin/env python
# encoding: utf-8

from Observer import Observer
from Subject import Subject
from Select import Selector
from Listen import Listener
import support2
#import os

import unittest
import os
from FTP import FTPFactory
from time import sleep
from Getor import NewGetor
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

def ToDict(sque, k=0, v=1, reverse=False):
# sque 需要是以二(或更高)元组作为元素的序列, 否则会raise ValueError, 或TypeError
# 如果元素高于二元组则只会取k(ey), v(alue)元素分别作为(dict的)键值对
    if sque and len(sque[0]) < 2:
        raise ValueError("sque's item is not two-tuples(or more).")

    if reverse:
        k, v = v, k

    return dict(map(lambda t: (t[k], t[v]), sque))


class FileTableFactory(object):
    def __init__(self, ftp):
        super(FileTableFactory, self).__init__()
        self._ftp = ftp
        self._factoryList = []

    def New(self, root='/', parent=object):
        #print(root)
        listener = Listener(self._ftp, root)
        fileTable = FileTable(root, parent, self)

        listener.Attach(fileTable) # binding Listener
        listener.start()

        self._factoryList.append((listener, fileTable))

        return fileTable

    def Delete(self, fileTable):
        for apple in self._factoryList:
            if apple[1] == fileTable:
                apple[0].Detach(fileTable)
                #apple[1]._KillSelf()
                del self._factoryList[self._factoryList.index(apple)]
                break

    @property
    def Listener(self):
        return [l for l, r in self._factoryList]

    @property
    def FTP(self):
        return self._ftp


class FileTable(Observer, Subject):
    def __init__(self, root, parent, factory):
        #super(FileTable, self).__init__()
        Observer.__init__(self)
        Subject.__init__(self)

        self._root = root
        self._parent = parent
        self._factory = factory

        self._fileHash = dict()
        self._dirHash = dict()

        self._fileSelector = Selector(r"^\s*(\d+) (.*)$")
        self._dirSelector = Selector(r"^\s*(.*)/$")

    def Update(self, info):
        try:
            #self.GetDirList()
            ftpFileHash = ToDict(self._fileSelector.Findall(info), reverse=True) # Notice!
            ftpDirSet = set(self._dirSelector.Findall(info))

            if self._fileHash !=  ftpFileHash:
                self._fileHash = ftpFileHash
                fileSet = set()
                for k, v in self._fileHash.items():
                    fileSet.add(tuple([support2.Join(self._root, k), v]))

                try:
                    #print(fileSet)
                    self.Notify(fileSet)
                except IOError as e:
                    print("[IOError]: {} killself".format(self._root))
                    self._KillSelf
                    raise e

            detachSet = set(self._dirHash.keys()) - ftpDirSet
            attachSet = ftpDirSet - set(self._dirHash.keys())

            for aDir in attachSet:
                # new FileTable
                self._dirHash[aDir] = self._factory.New(support2.Join(self._root, aDir), # root
                                                        self)                            # parent

            for aDir in detachSet:
                # Delete FileTable
                self._factory.Delete(self._dirHash[aDir])
                del self._dirHash[aDir]
        finally:
            #print(self.GetDirList())
            #print(self.GetFileList())
            pass

    def Notify(self, info):
        if self._parent != object:
            self._parent.Notify(info)
        else:
            super(FileTable, self).Notify(info)

    def GetDirList(self):
        cDir = self._root
        if support2.Version() == 2:
            cDir = unicode(self._root)

        dirList = [cDir]

        for fileTable in self._dirHash.values():
            dirList += fileTable.GetDirList()

        return dirList

    def GetFileList(self):
        fileList = []

        for aFile in self._fileHash.keys():
            fileList.append(support2.Join(self._root, aFile))

        for fileTable in self._dirHash.values():
            fileList += fileTable.GetFileList()

        return fileList

    @property
    def FTP(self):
        return self._factory.FTP


class FileListTest(unittest.TestCase):
    def setUp(self):
        self.CreateFtpInfo()
        ftp = FTPFactory().GetFTP()
        self.fileList = FileTableFactory(ftp).New()
        self.fileList.Attach(NewGetor(ftp, "abc"))
        c = 0
        l = _threading.activeCount()
        #while c != l:
        #    c = l
        #    sleep(1)
        #    l = _threading.activeCount()
        sleep(2)
        self.maxDiff = None

    def tearDown(self):
        self.RemoveFtpInfo()
        pass

    def test_GetDirList(self):
        testDirList = map(lambda s: s.replace(u'/home/ftp/', '/'), self.RGetDir(u'/home/ftp/'))
        if support2.Version() == 2:
            testDirList = map(unicode, testDirList)
        self.assertItemsEqual(self.fileList.GetDirList(), testDirList)
        pass

    def test_GetFileList(self):
        testFileList = map(lambda s: s.replace(u'/home/ftp/', '/'), self.RGetFile(u'/home/ftp/'))
        if support2.Version() == 2:
            testFileList = map(unicode, testFileList)
        self.assertItemsEqual(self.fileList.GetFileList(), testFileList)
        pass

    def CreateFtpInfo(self):
        info = r"""
        {
            "host": "ftp://192.168.1.102",
            "user": "anonymous",
            "passwd": "",
            "ssh": ""
        }
        """
        filename = 'ftpinfo.json'
        if os.path.exists(filename):
            os.rename(filename, filename + 'backup')
        with open(filename, 'w') as f:
            f.write(info)

    def RemoveFtpInfo(self):
        filename = 'ftpinfo.json'
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(filename + 'backup'):
            os.rename(filename + 'backup', filename)

    def RGetFile(self, dirName):
        dirList = os.listdir(dirName)
        fileList = []
        for f in dirList:
            if os.path.isdir(os.path.join(dirName, f)):
                fileList += self.RGetFile(os.path.join(dirName, f))
            else:
                fileList.append(os.path.join(dirName, f))

        return fileList

    def RGetDir(self, dirName):
        aList = os.listdir(dirName)
        dirList = [dirName]
        for d in aList:
            if os.path.isdir(os.path.join(dirName, d)):
                dirList += self.RGetDir(os.path.join(dirName, d))

        return dirList

def TestMain():
    unittest.main()

if __name__ == '__main__':
    TestMain()

