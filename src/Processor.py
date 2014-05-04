#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from os import system
from os import remove
from os.path import basename
from os import environ
from subprocess import call
from random import random
import platform


def RandomCode():
    return 'LittleKey'.join(str(random() * (10**8)).split('8'))[:80] + ".temp"

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
    def __init__(self, ftpLoginCM):
        self.ftpLoginCM = ftpLoginCM
        self.processorCM = \
r"""
lftp -f "{CONF_Filename}" > "{LOG_Filename}"
"""

    def _Execute(self, conffilename, logFilename):
        return system(self.processorCM.format(CONF_Filename=conffilename, \
                                              LOG_Filename=logFilename))

    def _Clean(self, *filenameList):
        for filename in filenameList:
            try:
                remove(filename)
            except NotImplementedError:
                print("Your platfrom not support remove.")
            except IOError:
                pass

    def __call__(self, command):
        inputFilename = RandomCode()
        outputFilename = RandomCode()

        with open(inputFilename, 'w') as confFile:
            confFile.write(self.ftpLoginCM)
            confFile.write(command)
            #print(command)
            #s=input()
        try:
            self._Execute(inputFilename, outputFilename)
            with open(outputFilename, encoding='utf-8') as outputFile:
                return outputFile.read()
        except IOError:
            print("[IOError]: No such file or directory: {}".format(settings.LOG_Filename))
            exit(0)
        finally:
            self._Clean(inputFilename, outputFilename)


class Win32Processor(Processor):
    """针对win32平台特性"""
    def __init__(self, ftpLoginCM):
        super(Win32Processor, self).__init__(ftpLoginCM)
        environ["PATH"] +=  ";" + settings.LFTP_DIR


class LinuxProcessor(Processor):
    """针对linux平台特性"""
    def __init__(self, ftpLoginCM):
        super(LinuxProcessor, self).__init__(ftpLoginCM)
        environ["PATH"] += ":" + settings.LFTP_DIR