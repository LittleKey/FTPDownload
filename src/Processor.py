#!/usr/bin/env python3
# encoding: utf-8

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
            print("Not support {} platfrom.".format(sysstr))
            raise SystemError

class Processor:
    def __init__(self, ftpLoginCM, processorCM):
        self.processorCM = processorCM
        self.ftpLoginCM = ftpLoginCM

    def __Execute(self):
        raise NotImplementedError

    def __Clean(self, filename):
        raise NotImplementedError

    def _Clean(self, filename):
        try:
            remove(filename)
        except NotImplementedError:
            print("Your platfrom not support remove.")

    def __call__(self, command, filename):
        raise NotImplementedError

class Win32Processor(Processor):
    def __init__(self, ftpLoginCM, processorCM=settings.CM_Execute_Win32):
        super(Win32Processor, self).__init__(ftpLoginCM, processorCM)

    def __Execute(self, filename=RandomCode()):
        filename = filename + '.cmd'
        with open(filename, 'w') as execFile:
            execFile.write(self.processorCM)

        try:
            call([filename])
        finally:
            self.__Clean(filename)

    def __Clean(self, filename):
        super(Win32Processor, self)._Clean(filename)

    def __call__(self, command, filename=settings.CONF_Filename):
        with open(filename, 'w') as confFile:
            confFile.write(self.ftpLoginCM)
            confFile.write(command)
        try:
            self.__Execute()
        finally:
            self.__Clean(filename)



class LinuxProcessor(Processor):
    def __init__(self, ftpLoginCM, processorCM=settings.CM_Execute_Linux):
        super(LinuxProcessor, self).__init__(ftpLoginCM, processorCM)

    def __Execute(self):
        system(self.processorCM)

    def __Clean(self, filename):
        super(LinuxProcessor, self)._Clean(filename)

    def __call__(self, command, filename=basename(settings.CONF_Filename)):
        with open(filename, 'w') as confFile:
            confFile.write(self.ftpLoginCM)
            confFile.write(command)
        try:
            self.__Execute()
        finally:
            self.__Clean(filename)
