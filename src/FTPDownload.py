#!/usr/bin/env python3
#encoding: utf-8

################
#              #
#   程序入口   #
#              #
################

__Author__ = 'LittleKey (LittleKeyRain@gmail.com)'
__Version__ = '3.0'
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
下载完成后会自动关闭
如果使用 至少需要设置lftp所在的目录
更多设置见 settings.py 文件


[Requirements]
    Python 2.6 (or more later)
    lftp (need cygwin for windows)

[USAGE]

    FTPDownload.py AnimeName [num] [-t TV]

    AnimeName
        动画名

""".format(Author=__Author__, Version=__Version__)

from main import main
from main import Clear
from sys import argv
import settings
import support2.py

if __name__ == '__main__':
    if support2.CheckVersion():
        print("[VersionError]: Your Python version is {}".format(\
                                            '.'.join(map(str, version_info[:3]))))
        exit(-1)

    apple = 0
    TV = ''
    try:
        if '-T' in argv:
            num = argv.index('-T')
            del argv[num]
            TV = argv.pop(num)

        if len(argv) == 3:
            main(argv[1], int(argv[2]), TV=TV)
        elif len(argv) == 2:
            main(argv[1], TV=TV)
        else:
            print(__doc__)
            exit(-1)

    finally:
        Clear(settings.LOG_Filename)
