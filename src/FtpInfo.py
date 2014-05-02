#!/usr/bin/env python3
# encoding: utf-8

import settings
from getpass import getpass


class FtpInfo:
    def __init__(self, host='', user='', passwd='', ssh=''):
        self.info = {
            'host':    host,
            'user':    user,
            'passwd':  passwd,
            'ssh':     ssh
        }

    def __getitem__(self, key):
        return self.info.get(key)

    def __setitem__(self, key, value):
# 用于修改ftp的信息
# 如果输入的key不存在info里则会raise TypeError
        if key in self.info.keys():
            self.info[key] = value
        else:
            raise TypeError

    def GetInfo(self):
        try:
            self.__GetInfoFromFile()
        except IOError:
            self.__GetInfoFromInput()

    def __GetInfoFromFile(self, ftpConf=settings.FTP_Conf_File):
        # 从配置文件获取
        with open(ftpConf) as ACFile:
            self.info['host'] = ACFile.readline().strip()
            self.info['user'] = ACFile.readline().strip()
            self.info['passwd'] = ACFile.readline().strip()
            self.info['ssh'] = ACFile.readline().strip()

    def __GetInfoFromInput(self):
        # 如果没有配置文件，则改为手动输入
        self.info['host'] = input("host: ")
        self.info['user'] = input("account: ")
        self.info['passwd'] = getpass("password: ")
        self.info['ssh'] = input("SSH: ")

    def SetInfoFromFile(self):
        self.__GetInfoFromFile()

    def SetInfoFromInput(self):
        self.__GetInfoFromInput()
