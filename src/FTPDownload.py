#!/usr/bin/env python
#encoding: utf-8

################
#              #
#   程序入口   #
#              #
################

from __future__ import print_function

__Author__ = 'LittleKey (LittleKeyRain@gmail.com)'
__Version__ = '4.3'
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

""".format(Author=__Author__, Version=__Version__)


from main import main, NewMain
from main import Clear
#from sys import argv
import argparse
from sys import version_info
import settings
import support2
from os import listdir
from os.path import abspath

if __name__ == '__main__':
    if support2.CheckVersion():
        print("[VersionError]: Your Python version is {}".format(\
                                            '.'.join(map(str, version_info[:3]))))
        exit(-1)

    try:
        parser = argparse.ArgumentParser(description="FTP Downloader, support Regular Expression. base on lftp")
        parser.add_argument('-n', '--new', action="store_true", default=False, help="Use new version.")
        parser.add_argument('-i', '--info', default=settings.FTP_Conf_File, help="Set ftp info file path.")
        parser.add_argument('-p', '--path', default=settings.LFTP_DIR, help="Set lftp ENV.")
        parser.add_argument('-dd', '--downloadDir', default=settings.Download_Dir, help="Set Download directory.")
        parser.add_argument('match', metavar='M',  nargs='+', help="Download filename, support Regular Expression.\
                                                                    use '/' split directory.")

        args = parser.parse_args()

        settings.LFTP_DIR = abspath(args.path)
        settings.FTP_Conf_File = abspath(args.info)
        settings.Download_Dir = abspath(args.downloadDir)

        if args.new:
            NewMain(args.match)
        else:
            main(args.match)
    finally:
        Clear(*[x for x in listdir('.') if x.endswith(r".temp")])
