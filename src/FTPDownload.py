#!/usr/bin/env python
#encoding: utf-8

################
#              #
#   程序入口   #
#              #
################

from __future__ import print_function

__Author__ = 'LittleKey (LittleKeyRain@gmail.com)'
__Version__ = '4.1'
__doc__ = \
r"""
#####################
#                   #
#    FTPDownload    #
#                   #
#####################

by: {Author}
ver: {Version}

自动从ftp下载ts
采用轮询检查是否更新
支持使用正则表达式进行批量下载
如果使用 至少需要设置lftp所在的目录
更多设置见 settings.py 文件


[Requirements]
    Python 2.6 (or more later)
    lftp (need cygwin for windows)

[USAGE]

    FTPDownload.py AnimeName [moreAnimeName] [-n]

    AnimeName [moreAnimeName]
        动画名， 使用正则表达式匹配。会下载所有匹配的文件。
        可以输入多个，并附带(FTP上的)目录名, 使用 '/' 分隔。
        目录默认为'/': 'dirname/basename' == '/dirname/basename'

""".format(Author=__Author__, Version=__Version__)


from main import main, NewMain
from main import Clear
from sys import argv
from sys import version_info
#import settings
import support2
from os import listdir

if __name__ == '__main__':
    if support2.CheckVersion():
        print("[VersionError]: Your Python version is {}".format(\
                                            '.'.join(map(str, version_info[:3]))))
        exit(-1)

    try:
        if '-n' in argv:
            del argv[argv.index('-n')]
            NewMain(argv[1:])
        else:
            main(argv[1:])
    finally:
        Clear(*[x for x in listdir('.') if x.endswith(r".temp")])
