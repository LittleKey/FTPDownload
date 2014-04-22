#!/usr/bin/env python3
# encoding: utf-8


class FtpInfo:
    def __init__(self, host, user, passwd, ssh):
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
