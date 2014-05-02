#!/usr/bin/env python3
# encoding: utf-8

#import settings
import re


class Selector:
    """貌似只是超简单的封装了一下re库..."""
    def __init__(self, match, flag=re.I | re.M):
        self.match = re.compile(match, flag)

    def Findall(self, context):
        #print(context)
        return self.match.findall(context)
