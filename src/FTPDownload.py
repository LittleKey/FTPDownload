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
    Python 3.3.5 (or more later)
    lftp (need cygwin for windows)

[USAGE]

    FTPDownload.py AnimeName [num] [-t TV]

    AnimeName
        动画名

    num [dafault: 0]
        指定要下集数的范围
        下载集数的范围是[num-last]
        p.s: 只会下最新一集

    -t
        指定要选择的电视台

    TV [default: '']
        电视台名

""".format(Author=__Author__, Version=__Version__)

from main import main
from main import Clear
from sys import argv
import settings
from sys import version_info


def CheckVersion():
    pyver_local = version_info[:3]
    pyver_need = (3, 3, 5)

    return pyver_local < pyver_need

if __name__ == '__main__':
    if CheckVersion():
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
