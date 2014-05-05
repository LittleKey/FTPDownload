#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function


class Observer(object):
    def __init__(self):
        self.alive = True

    def Update(self, info):
        raise NotImplementedError

    def WantAlive(self):
        return self.alive

    def _KillSelf(self):
        self.alive = False
