#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import os

"""统计目录下所有匹配文件的行数."""

def GetFileList(cdir):
    return filter(lambda t: os.path.isfile(os.path.join(cdir, t)), os.listdir(cdir))

def GetDirList(cdir):
    if cdir:
        currentDirs = filter(lambda t: os.path.isdir(t), \
            map(lambda t: os.path.join(cdir, t), os.listdir(cdir)))
# 获取子目录
        for cDir in currentDirs:
            currentDirs += GetDirList(cDir)

        return currentDirs

def CountOneDir(inputDir):
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

    return total

if __name__ == '__main__':
    inputDir = '.'
    rFlag = False
    try:
        num = sys.argv.index('-r')
        del sys.argv[num]
        rFlag = True
    except ValueError:
        rFlage = False

    if len(sys.argv) == 3:
        inputDir = sys.argv.pop()
    if len(sys.argv) == 2:
        expr = sys.argv.pop()
    else:
        print("[InputError]: Input arguments has errors..")
        exit(0)

    match = re.compile(expr, re.IGNORECASE)

    dirList = []
    if rFlag:
        dirList = GetDirList(inputDir)
    dirList.append(inputDir)

    total = 0
    for cdir in dirList:
        total += CountOneDir(cdir)

    print("Line total is {total}".format(total=total))
