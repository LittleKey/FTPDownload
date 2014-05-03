#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from os import system
from os import remove
from os.path import basename
from subprocess import call
from random import random
import platform


def RandomCode():
    return 'LittleKey'.join(str(random() * (10**8)).split('8'))[:80]

class ProcessorFactory:
    """"return 'Processor' class"""
    def __init__(self, loginCM):
        self.ftpLoginCM = loginCM

    def GetProcessor(self):
        sysstr = platform.system().lower()

        if sysstr == 'linux':
            return LinuxProcessor(self.ftpLoginCM)
        elif sysstr == 'windows':
            return Win32Processor(self.ftpLoginCM)
        else:
            print("Not support '{}' platfrom.".format(sysstr))
            raise SystemError

class Processor:
    def __init__(self, ftpLoginCM, processorCM):
        self.processorCM = processorCM
        self.ftpLoginCM = ftpLoginCM

    def _Execute(self):
        raise NotImplementedError

    def _Clean(self, filename):
        try:
            remove(filename)
        except NotImplementedError:
            print("Your platfrom not support remove.")
        except IOError:
            pass

    def __call__(self, command, filename):
        with open(filename, 'w') as confFile:
            confFile.write(self.ftpLoginCM)
            confFile.write(command)
        try:
            self._Execute()
        finally:
            self._Clean(filename)


class Win32Processor(Processor):
    def __init__(self, ftpLoginCM, processorCM=settings.CM_Execute_Win32):
        super(Win32Processor, self).__init__(ftpLoginCM, processorCM)

    def _Execute(self, filename=RandomCode()):
        filename = filename + '.cmd'
        with open(filename, 'w') as execFile:
            execFile.write(self.processorCM)

        try:
            call([filename])
        finally:
            self._Clean(filename)

    def __call__(self, command, filename=settings.CONF_Filename):
        # 坑爹的父类方法调用方式
        super(Win32Processor, self).__call__(command, filename)


class LinuxProcessor(Processor):
    def __init__(self, ftpLoginCM, processorCM=settings.CM_Execute_Linux):
        super(LinuxProcessor, self).__init__(ftpLoginCM, processorCM)

    def _Execute(self):
        system(self.processorCM)

    def __call__(self, command, filename=basename(settings.CONF_Filename)):
        # 坑爹的父类方法调用方式
        super(Win32Processor, self).__call__(command, filename)