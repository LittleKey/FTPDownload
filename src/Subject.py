#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function


class Subject(object):
    def __init__(self):
        self.observersSet = set()

    def Attach(self, o):
        self.observersSet.add(o)

    def Detach(self, o):
        try:
            self.observersSet.remove(o)
        except KeyError as e:
            print("[KeyError]: {} Observer is not exists in {} Subject".format(o.__class__, self.__class__))

    def Notify(self, info=''):
        detachList = []
        for observer in self.observersSet:
            try:
                if observer.WantAlive():
                    observer.Update(info)
                else:
                    detahList.append(observer)

            except NameError as e:
                print("[NameError]: {}".format(e.message))
                detachList.append(observer)
            except NotImplementedError as e:
                print("[NotImplementedError]: {}".format(e.message))
                detachList.append(observer)
            except AttributeError as e:
                print("[AttributeError]: {}".format(e.message))
                detachList.append(observer)

        for observer in detachList:
            self.Detach(observer)

        if not self.HasElements():
            raise IOError("Subject is not any observers.")

    def HasElements(self):
        return len(self.observersSet) != 0
