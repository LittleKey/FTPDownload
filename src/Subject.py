#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from support2 import Version


class Subject(object):
    def __new__(cls, *args, **kwgs):
        # 用于支持Mixin
        cls.observersSet = set()

        if Version() == 2:
            return super(Subject, cls).__new__(cls, *args, **kwgs)
        else:
            return super(Subject, cls).__new__(cls)

    def Attach(self, o):
        self.observersSet.add(o)

    def Detach(self, o):
        try:
            self.observersSet.remove(o)
        except KeyError:
            pass

    def Notify(self, info=''):
        detachList = []
        for observer in self.observersSet:
            try:
                if observer.WantAlive():
                    observer.Update(info)
                else:
                    detahList.append(observer)

            except NameError:
                detachList.append(observer)
            except NotImplementedError:
                detachList.append(observer)
            except AttributeError:
                detachList.append(observer)

        for observer in detachList:
            self.Detach(observer)

        if self.observersSet == set():
            raise IOError

    def HasElements(self):
        return len(self.observersSet) != 0
