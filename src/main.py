#!/usr/bin/env python3
#encoding: utf-8

__Author__ = 'LittleKey'
__Version__ = '1.2'
__doc__ = \
"""
FTP downloader
"""

import os
import settings
from getpass import getpass
from Select import Selector
from FtpInfo import FtpInfo
from FTP import FTPFactory
from StringMerge import StringMerge
from time import sleep


class Listener:
    def __init__(self, **kwargs):
        self.fileInfo = {}
        for key in kwargs.keys():
            self.fileInfo[key] = kwargs[key]

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

        return FtpInfo(host=host, user=account, passwd=password, ssh=SSH)

    def SetFtp(self):
        ftpInfo = self.__GetFtpInfo(settings.FTP_Conf_File)
        self.ftp = FTPFactory(ftpInfo)

    def SetSelector(self, match):
        self.selector = Selector(match)

    def __Download(self, filename, size, downloadDir=settings.Download_Dir):
        try:
            return self.ftp.GetFile(filename, size, downloadDir)
        except NameError:
# 我想大概不会变成无限递归吧...
            self.SetFtp()
            return self.__Download(filename, size, downloadDir)

    def __GetList(self):
        try:
            return self.selector.Findall(self.ftp.GetList())
        except NameError:
            self.SetFtp()

    def Listen(self):
# 保护继承
        print("[Warning]: Please inheritance(cover) Listen method.")
        print("[Warning]: Care unlimited recursive.")


class CK(Listener):
    def __init__(self, animeName, num='0', TV=''):
        self.__init__(name=str(animeName), num=str(num), TV=str(TV))

    def __GetFtpInfo_CK(self, ftpConf):
        """maybe this isn't useful..."""
        ftpInfo = self.__GetFtpInfo(ftpConf)
        if ftpInfo['ssh'] == '':
            # SSh默认设为TLS_V1
            ftpInfo['ssh'] = "TLS_V1"

            return ftpInfo

    def SetSelector_CK(self, match=r'group   (\d.*) \w+\w+\w+.*? {}_?(\d*)_?(.*?)\.ts'):
        r"""使用正则表达式进行匹配，默认的RE只用于处理CK片源服的ts list"""
# 大小, 集数, 电视台
        self.SetSelector(match.format(self.fileInfo['name']))

    def __Download_CK(self, filename, size, downloadDir=settings.Download_Dir):
        flag = 0
        while flag != 2:
            # 直到下载完成前会一直循环。。。出问题了的话就强关吧。。。
            flag = self.__Download(filename, size, downloadDir)


    def Listen(self, num=True, TV=False):
        r"""监听"""
        while True:
            tsList = self.__GettsList()
# 过滤器
            if TV and self.fileInfo['TV']:
                tsList = list(filter(lambda t: t[2].upper() == self.fileInfo['TV'], tsList))

            if num and self.fileInfo['num']:
                tsList = list(filter(lambda t: int(t[1]) >= self.fileInfo['num'], tsList))

            if tsList:
                size, num, TV = sorted(tsList, key=lambda t: t[1])[-1]
                filename =  StringMerge( \
                        head=self.fileInfo['name'], \
                        foot='.ts', \
                        middleWare='_', \
                        stringList=[num, TV]\
                    ).Return()

                print(r"{} size: {}".format(filename, size))
                self.__Download_CK(filename, int(size))
                break
            else:
                print("{} {} 第{}集 尚未更新，5分钟后再次检查...".format( \
                                                    self.fileInfo['name'], \
                                                    self.fileInfo['TV'], \
                                                    self.fileInfo['num']) \
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
    ck = CK(animeName, num, TV)
    ck.SetFtp(ck.__GetFtpInfo_CK(settings.FTP_Conf_File))
    ck.SetSelector_CK()

    TV = not not TV
    ck.Listen(TV=TV)
