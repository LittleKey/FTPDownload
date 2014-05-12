#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from getpass import getpass
from json import loads
from support2 import Input


class FtpInfo(object):
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
        try:
            with open(ftpConf) as confFile:
                self.info.update(loads(confFile.read()))
        except ValueError:
            print("[ValueError]: '{}' is not json data.".format(ftpConf))
            print("Please input in stdin...")
            raise IOError

    def __GetInfoFromInput(self):
        # 如果没有配置文件，则改为手动输入
        self.info['host'] = Input("host: ")
        self.info['user'] = Input("account: ")
        self.info['passwd'] = getpass("password: ")
        self.info['ssh'] = Input("SSH: ")

    def SetInfoFromFile(self):
        self.__GetInfoFromFile()

    def SetInfoFromInput(self):
        self.__GetInfoFromInput()
