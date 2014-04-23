#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import os

"""统计目录下所有匹配文件的行数."""

def GetFileList(cdir):
    return os.listdir(cdir)

if __name__ == '__main__':
    inputDir = '.'
    if len(sys.argv) == 3:
        inputDir = sys.argv.pop()
    if len(sys.argv) == 2:
        expr = sys.argv.pop()
    else:
        print("[InputError]: Input arguments has errors..")
        exit(0)

    match = re.compile(expr, re.IGNORECASE)
    fileList = GetFileList(inputDir)

    matchList = list(filter(match.match, fileList))

    absFileList = list(map(lambda t: \
                            os.path.abspath( \
                                os.path.join(inputDir, t) \
                            ), \
                        matchList))

    total = 0
    for filename in absFileList:
        with open(filename) as aFile:
            total += len(list(aFile.readlines()))

    print("Line total is {total}".format(total=total))
