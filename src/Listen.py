#!/usr/bin/env python
# encoding: utf-8


import settings
from getpass import getpass
from FtpInfo import FtpInfo
from Select import Selector
from FTP import FTPFactory


class Listener:
    def __init__(self, match=r'.*'):
        self.__SetFtp()
        self.__SetSelector(match)

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

    def __SetFtp(self):
        ftpInfo = self.__GetFtpInfo(settings.FTP_Conf_File)
        self.ftp = FTPFactory(ftpInfo).GetFTP()

    def __SetSelector(self, match):
        self.selector = Selector(match)

    def Download(self, filename, size, downloadDir=settings.Download_Dir):
        return self.ftp.GetFile(filename, size, downloadDir)

    def __GetList(self):
        return self.selector.Findall(self.ftp.GetList())

    def Listen(self):
        return self.__GetList()

