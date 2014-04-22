#!/usr/bin/env python3
#encoding: utf-8

__Author__ = 'LittleKey'
__Version__ = '1.1'
__doc__ = \
"""
FTP downloader
"""

import os
import settings
from getpass import getpass
from Select import Selector
from FtpInfo import FtpInfo
from FTP import FTP
from StringMerge import StringMerge
from time import sleep


class CK_BaS:
    def __init__(self, animeName=r'Blade_and_Soul', num=0, TV='TBS'):
        self.animeInfo = {
                'name': animeName,
                'num': int(num),
                'TV': TV
            }

    def __GetFtpInfo(self, ftpConf):
        try:
            # 从配置文件获取
            with open(ftpConf) as ACFile:
                host = ACFile.readline().strip()
                account = ACFile.readline().strip()
                password = ACFile.readline().strip()
                SSH = ACFile.readline().strip()
        except FileNotFoundError:
            # 如果没有配置文件，则改为手动输入
            host = input("host: ")
            account = input("account: ")
            password = getpass("password: ")
            SSH = input("SSH[default: TLS_V1]: ")
        #finally:
        #    print("{}, {}, {}, {}".format(host, account, password, SSH))

        if SSH == '':
            SSH = "TLS_V1"

        return FtpInfo(host=host, user=account, passwd=password, ssh=SSH)

    def SetFtp(self):
        ftpInfo = self.__GetFtpInfo(settings.FTP_Conf_File)
        self.ftp = FTP(ftpInfo)

    def SetSelector(self, match=r'group   (\d.*) \w+\w+\w+.*? {}_?(\d*)_?(.*?)\.ts'):
# 大小, 集数, 电视台
        self.selector = Selector(match.format(self.animeInfo['name']))

    def __Download(self, filename, size, downloadDir=settings.Download_Dir):
        flag = 0
        while flag != 2:
            flag = self.ftp.GetFile(filename, size, downloadDir)

    def __GettsList(self):
        return self.selector.Findall(self.ftp.GetList())

    def Listen(self, num=True, TV=False):
        while True:
            basList = self.__GettsList()
# 过滤器
            if TV and self.animeInfo['TV']:
                basList = list(filter(lambda t: t[2].upper() == self.animeInfo['TV'], basList))

            if num and self.animeInfo['num']:
                basList = list(filter(lambda t: int(t[1]) >= self.animeInfo['num'], basList))

            if basList:
                size, num, TV = sorted(basList, key=lambda t: t[1])[-1]
                filename =  StringMerge( \
                        head=self.animeInfo['name'], \
                        foot='.ts', \
                        middleWare='_', \
                        stringList=[num, TV]\
                    ).Return()

                print(r"{} size: {}".format(filename, size))
                self.__Download(filename, int(size))
                break
            else:
                print("{} {} 第{}集 尚未更新，5分钟后再次检查...".format( \
                                                    self.animeInfo['name'], \
                                                    self.animeInfo['TV'], \
                                                    self.animeInfo['num']) \
                                                    )
                sleep(5*60)

def Clear(*args):
    # 清理文件
    for aFile in args:
        try:
            os.remove(aFile)
        except FileNotFoundError:
            print("No such file {}".format(aFile))
        except NotImplementedError:
            print("Your platform not support remove.")
            return -1

def main(animeName, num=0, TV=''):
    bas = CK_BaS(animeName, num, TV)
    bas.SetFtp()
    bas.SetSelector()

    TV = not not TV
    bas.Listen(TV=TV)
