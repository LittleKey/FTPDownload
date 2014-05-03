#!/usr/bin/env python3
# encoding: utf-8

import sys
import re
import os

"""统计目录下所有匹配文件的行数."""

def GetFileList(cdir):
    return filter(lambda t: os.path.isfile(os.path.join(cdir, t)), os.listdir(cdir))

def GetDirList(cdir):
    currentDirs = list(filter(lambda t: os.path.isdir(t), \
        map(lambda t: os.path.join(cdir, t), os.listdir(cdir))))
# 获取子目录
    for cDir in currentDirs:
        currentDirs += GetDirList(cDir)

    return currentDirs

def CountOneDir(inputDir, lFlag):
    fileList = GetFileList(inputDir)

    matchList = list(filter(match.match, fileList))

    absFileList = list(map(lambda t: \
                            os.path.abspath( \
                                os.path.join(inputDir, t) \
                            ), \
                        matchList))

    total = 0
    for filename in absFileList:
        try:
            with open(filename, encoding='utf-8') as aFile:
                num = len(list(aFile.readlines()))
                if lFlag:
                    print("{num} line in {filename}".format(num=num, filename=filename))
                total += num
        except UnicodeDecodeError:
            print("[IOError]: Can't open file '{}'.".format(filename))                

    return total

if __name__ == '__main__':
    inputDir = '.'
    rFlag = False # 是否递归的flag
    lFlag = False # 是否列出被计算的文件
    try:
        num = sys.argv.index('-r')
        del sys.argv[num]
        rFlag = True
    except ValueError:
        rFlage = False

    try:
        num = sys.argv.index('-l')
        del sys.argv[num]
        lFlag = True
    except ValueError:
        lFlage = False

    if len(sys.argv) == 3:
        inputDir = sys.argv.pop()
    if len(sys.argv) == 2:
        expr = sys.argv.pop()
    else:
        print("[InputError]: Input arguments has errors..")
        exit(0)

# 使用正则表达式匹配
    match = re.compile(expr, re.IGNORECASE)
    if not os.path.exists(inputDir):
        print("[FileNotFoundError]: No such file '{}'".format(inputDir))
        exit(0)
 
    dirList = [inputDir]
    if rFlag:
# 递归处理所以子目录(谨慎使用...)
        dirList += GetDirList(inputDir)
    dirSet = set(dirList) # 使用集合 去掉重复的目录

    total = 0
    for cdir in dirSet:
        total += CountOneDir(cdir, lFlag)

    print("\nLine total is {total}".format(total=total))