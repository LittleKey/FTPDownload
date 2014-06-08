#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from sys import version_info


def CheckVersion():
    pyver_local = version_info[:2]
    pyver_need = (2, 6)

    return pyver_local < pyver_need

def Input(context):
    try:
        return raw_input(context)
    except NameError:
        return input(context)

def Version():
    return version_info[0]
