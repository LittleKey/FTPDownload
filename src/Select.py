#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
#import settings
import re


class Selector(object):
    """貌似只是超简单的封装了一下re库..."""
    def __init__(self, match, flag=re.I | re.M, log=None):
        try:
            self._match = re.compile(match, flag)
        except re.error as e:
            print("[REError]: " + e.message)
            raise TypeError("Regular Expression has any error.")
        finally:
            if log:
                print("[Regular Expression]:", end=' ')
                print(self._match.pattern, file=log)

    def Findall(self, context):
        #print(context)
        return self._match.findall(context)

    def Match(self, context):
        return self._match.match(context)
