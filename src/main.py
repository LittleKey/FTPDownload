#!/usr/bin/env python3
#encoding: utf-8

import os
import settings
from StringMerge import StringMerge
from time import sleep
from Listen import Listener


class CK:
    def __init__(self, animeName, num=0, TV='', match=''):
        self.listener = Listener(match)
        self.animeInfo = {
                'name': animeName,
                'num': num,
                'TV': TV
            }

    def __Download(self, filename, size, downloadDir=settings.Download_Dir):
        flag = 0
        while flag != 2:
            # 直到下载完成前会一直循环。。。出问题了的话就强关吧。。。
            flag = self.listener.Download(filename, size, downloadDir)

    def __Filter(self, tsList, num, TV):
# 过滤器
        if tsList and TV and self.animeInfo['TV']:
            tsList = list(filter(lambda t: t[2].upper() == self.animeInfo['TV'], tsList))

        if tsList and num and self.animeInfo['num']:
            tsList = list(filter(lambda t: int(t[1]) >= self.animeInfo['num'], tsList))

        return tsList

    def Listen(self, num=True, TV=False):
        r"""监听"""
        while True:
            tsList = self.__Filter(self.listener.Listen(), num, TV)

            if tsList:
                size, num, TV = sorted(tsList, key=lambda t: t[1])[-1]
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
    ck = CK(animeName, num, TV, match='group   (\d.*) \w+\w+\w+.*? {}_?(\d*)_?(.*?)\.ts'.format(animeName))

    TV = not not TV
    ck.Listen(TV=TV)
