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
            raise TypeError("FTP no '{key}' info.".format(key=key))

    def GetInfo(self):
        try:
            self.__GetInfoFromFile(settings.FTP_Conf_File)
        except IOError as e:
            print("[IOError]: {message}".format(e.message))
            print("Please input in stdin...")
            self.__GetInfoFromInput()

    def __GetInfoFromFile(self, ftpConf):
        # 从配置文件获取
        try:
            with open(ftpConf) as confFile:
                self.info.update(loads(confFile.read()))
        except ValueError as e:
            print("[ValueError]: {}".format(e))
            raise IOError("'{file}' is not json data".format(e.message, file=ftpConf))

    def __GetInfoFromInput(self):
        # 如果没有配置文件，则改为手动输入
        self.info['host'] = Input("host: ")
        self.info['user'] = Input("account: ")
        self.info['passwd'] = getpass("password: ")
        self.info['ssh'] = Input("SSH: ")

    def SetInfoFromFile(self, path=settings.FTP_Conf_File):
        self.__GetInfoFromFile(path)

    def SetInfoFromInput(self):
        self.__GetInfoFromInput()
