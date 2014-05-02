#!/usr/bin/env python3
# encoding: utf-8

from sys import version_info
try:
	from __future__ import print_function
except ImportError:
	print("[VersionError]: Your Python version is {}".format(\
                                            '.'.join(map(str, version_info[:3]))))
        exit(-1)

def CheckVersion():
    pyver_local = version_info[:2]
    pyver_need = (2, 6)

    return pyver_local < pyver_need