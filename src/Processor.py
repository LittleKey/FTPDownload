#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from os import system
from os import remove
from os.path import exists
#from os.path import basename
#from subprocess import call
from random import random
import platform
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class FilenameFactory(object):
    def __init__(self, lock=_threading.Lock()):
        self._lock = lock

    def Get(self):
        return Filename(self._lock)


class Filename:
    def __init__(self, lock=_threading.Lock()):
        self._lock = lock

    def GetFilename(self):
        if self._lock.acquire():
            filename = self.RandomCode()
            if self.isExists(filename):
                if self._lock.locked():
                    self._lock.release()
                return self.GetFilename()
            else:
                if self._lock.locked():
                    self._lock.release()
                return filename

    def RandomCode(self):
        return 'LittleKey'.join(str(random() * (10**8)).split('8'))[:80] + ".temp"

    def isExists(self, filename):
        return exists(filename)

def RandomCode():
    return 'LittleKey'.join(str(random() * (10**8)).split('8'))[:80] + ".temp"


class ProcessorFactory(object):
    """"return 'Processor' class"""
    def __init__(self, loginCM, filenameFactory=FilenameFactory()):
        self.ftpLoginCM = loginCM
        self._filename = filenameFactory.Get()

    def GetProcessor(self):
        sysstr = platform.system().lower()

        if sysstr == 'linux':
            return LinuxProcessor(self.ftpLoginCM, self._filename)
        elif sysstr == 'windows':
            return Win32Processor(self.ftpLoginCM, self._filename)
        else:
            print("Not support '{}' platfrom.".format(sysstr))
            raise SystemError

class Processor(object):
    def __init__(self, ftpLoginCM, filename):
        self.ftpLoginCM = ftpLoginCM
        self._filename = filename
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
            except OSError:
                pass

    def __call__(self, command):
        inputFilename = self._filename.GetFilename() #RandomCode()
        outputFilename = self._filename.GetFilename() #RandomCode()

        try:
            with open(inputFilename, 'w', encoding='utf-8') as confFile:
                confFile.write(self.ftpLoginCM)
                confFile.write(command)
        except TypeError:
            with open(inputFilename, 'w') as confFile:
                confFile.write(self.ftpLoginCM)
                confFile.write(command)

        try:
            self._Execute(inputFilename, outputFilename)
            with open(outputFilename, encoding='utf-8') as outputFile:
                return outputFile.read()
        except TypeError:
            with open(outputFilename) as outputFile:
                return outputFile.read().decode('utf-8')
        except IOError:
            print("[IOError]: No such file or directory: {}".format(settings.LOG_Filename))
            exit(0)
        finally:
            self._Clean(inputFilename, outputFilename)


class Win32Processor(Processor):
    """针对win32平台特性"""
    def __init__(self, ftpLoginCM, filename):
        super(Win32Processor, self).__init__(ftpLoginCM, filename)


class LinuxProcessor(Processor):
    """针对linux平台特性"""
    def __init__(self, ftpLoginCM, filename):
        super(LinuxProcessor, self).__init__(ftpLoginCM, filename)

