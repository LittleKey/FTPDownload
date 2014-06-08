#!/usr/bin/env python
# encoding: utf-8

from Observer import Observer
from Subject import Subject
from Select import Selector
from Listen import Listener
import os

def ToDict(sque, reverse=False):
# sque 需要是以二(或更高)元组作为元素的序列, 否则会raise ValueError, 或TypeError
# 如果元素高于二元组则只会取前两个元素分别作为(dict的)键值对
# 如有不同需求请修改 k(ey), v(alue) 对应的index
    if sque and len(sque[0]) < 2:
        raise ValueError

    k, v = 0, 1
    if reverse:
        k, v = v, k

    return dict(map(lambda t: (t[k], t[v]), sque))


class FileTableFactory(object):
    def __init__(self, ftp):
        super(FileTableFactory, self).__init__()
        self._ftp = ftp
        self._factoryList = []

    def New(self, root='/', parent=object):
        listener = Listener(self._ftp, root)
        fileTable = FileTable(root, parent, self)

        listener.Attach(fileTable) # binding Listener
        listener.start()

        self._factoryList.append((listener, fileTable))

        return fileTable

    def Delete(self, fileTable):
        for apple in self._factoryList:
            if apple[1] == fileTable:
                apple[0].__stop()
                apple[1].__KillSelf()
                del self._factoryList[self._factoryList.index(apple)]
                break

    @property
    def Listener(self):
        return [l for l, r in self._factoryList]


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
            ftpFileHash = ToDict(self._fileSelector.Findall(info), reverse=True) # Notice!
            ftpDirSet = set(self._dirSelector.Findall(info))

            if self._fileHash !=  ftpFileHash:
                self._fileHash = ftpFileHash
                fileSet = set()
                for k, v in self._fileHash.items():
                    fileSet.add(tuple([os.path.join(self._root, k), v]))

                self.Notify(fileSet)

            detachSet = set(self._dirHash.keys()) - ftpDirSet
            attachSet = ftpDirSet - set(self._dirHash.keys())

            for aDir in attachSet:
                # new FileTable
                self._dirHash[aDir] = self._factory.New(os.path.join(self._root, aDir), # root
                                                        self)                           # parent

            for aDir in detachSet:
                # Delete FileTable
                self._factory.Delete(self._dirHash[aDir])
                del self._dirHash[aDir]
        finally:
            pass

    def Notify(self, info):
        if self._parent != object:
            self._parent.Notify(info)
        else:
            super(FileTable, self).Notify(info)

    def GetDirList(self):
        dirList = [self._root]

        for fileTable in self._dirHash.values():
            dirList += fileTable.GetDirList()

        return dirList

    def GetFileList(self):
        fileList = []

        for aFile in self._fileHash.keys():
            fileList.append(os.path.join(self._root, aFile))

        for fileTable in self._dirHash.values():
            fileList += fileTable.GetFileList()

        return fileList


