#!/usr/bin/env python3
# encoding: utf-8

from __future__ import print_function
from sys import version_info


def CheckVersion():
    pyver_local = version_info[:2]
    pyver_need = (2, 6)

    return pyver_local < pyver_need