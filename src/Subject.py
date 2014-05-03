#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

class Subject:
    def __init__(self):
        self.observersSet = set()

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
                observer.Update(info)
            except NameError:
                detachList.append(observer)

        for observer in detachList:
            self.Detach(observer)

    def HasElements(self):
        return len(self.observersSet) != 0
