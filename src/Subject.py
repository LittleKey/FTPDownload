#!/usr/bin/env python3
# encoding: utf-8


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
        for observer in self.observersSet:
            observer.Update(info)

    def HasElements(self):
        return len(self.observersSet) != 0