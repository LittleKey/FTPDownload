#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from FtpInfo import FtpInfo
from Processor import ProcessorFactory
import os
from subprocess import call
#from sys import stdout
#from json import loads
import platform
from support2 import Version

def RMKDIR(path):
# 递归创建目录
    pPath = os.path.dirname(path)

    if not os.path.exists(pPath):
        #递归创建父目录
        RMKDIR(pPath)

    if not os.path.exists(path):
        os.mkdir(path)

class FTPFactory(object):
    def __init__(self, ftpInfo=FtpInfo()):
        if not isinstance(ftpInfo, FtpInfo):
            raise TypeError

        self.ftpInfo = ftpInfo
        self.ftpInfo.GetInfo()

    def GetFTP(self):
        # 暂时只有这一个FTP实现，所以这样写了...
        try:
            systemName = platform.system().lower()
            if systemName == "windows":
                os.environ["PATH"] +=  ";" + settings.LFTP_DIR
            elif systemName == "linux":
                os.environ["PATH"] += ":" + settings.LFTP_DIR

            print("Get lftp version...\n")
            call(['lftp', '--version'])

            return LFTP(self.ftpInfo)
        except IOError:
            print("[IOError]: No found lftp")
            exit(0)
        finally:
            print("\n")


class FTP(object):
    """其实这应该是抽象类...WTF!!"""
    def __init__(self, ftpInfo):
        if not isinstance(ftpInfo, FtpInfo):
            raise TypeError
        self.ftpInfo = ftpInfo

    def GetList(self, fileListDir):
        raise NotImplementedError

    def GetFile(self, filename, filesize, downloadDIR):
        raise NotImplementedError

    @property
    def host(self):
        return self.ftpInfo["host"]


class LFTP(FTP):
    r"""使用processor来处理各种lftp命令"""
    def __init__(self, ftpInfo):
        super(LFTP, self).__init__(ftpInfo)
        self.CM = settings.LFTP_CM_File

        self.processor = self.__SetProcessor(ftpInfo)

    def __SetProcessor(self,ftpInfo):
        loginCM = self.__GetLoginCM(ftpInfo)

        return ProcessorFactory(loginCM).GetProcessor()

    def __GetLoginCM(self, ftpInfo):
        loginCM = self.CM["CM_ftp_Login"].format(
                host   = ftpInfo['host'],
                user   = ftpInfo['user'],
                passwd = ftpInfo['passwd']
            )
        if ftpInfo['ssh'].upper() == "TLS_V1" or ftpInfo['ssh'].upper() == "SSL_V3":
            loginCM += self.CM["CM_ftp_Login_TLS_V1"]  # 添加TLS_V1验证设置。。。

        return loginCM

    def GetList(self, fileListDir):
        try:
            #print("\nGet list...", end='')
            #stdout.flush()
            if Version() == 2:
                fileListDir = fileListDir.encode("utf-8")

            return self.processor(self.CM["CM_ftp_List"].format(Dir=fileListDir))
        finally:
            pass
            #print("\r" + " "*len("Get list...") + "\r", end='')
            #print("Got list.", end='\n\n')

    def __GetNewFile(self, filename, downloadDIR, ftpDir):
        args = self.CM["ARGS_New_ts_Get"]
        filename = os.path.join(ftpDir, filename).replace('\\','/')

        return self.processor(self.CM["CM_LFTP_Get_File"].format(Download_Dir=downloadDIR, \
                                                               args=args, \
                                                               filename=filename))

    def __GetExistFile(self, filename, downloadDIR, ftpDir):
        args = self.CM["ARGS_Continue_ts_Get"]
        filename = os.path.join(ftpDir, filename).replace('\\','/')

        return self.processor(self.CM["CM_LFTP_Get_File"].format(Download_Dir=downloadDIR, \
                                                               args=args, \
                                                               filename=filename))

    def GetFile(self, filename, filesize, downloadDIR, ftpDir):
        fileExistDIR = os.path.abspath(os.path.join(downloadDIR + '/' + ftpDir)).replace('\\', '/')
        #print(fileExistDIR)
        RMKDIR(fileExistDIR)

        for cfile in os.listdir(fileExistDIR):
            if filename.lower() == cfile.lower():
                if os.path.getsize(os.path.join(fileExistDIR, filename)) >= int(filesize):
                    # 文件已存在，下载已完成
                    print("Download end.", end='\n\n')
                    return 2
                else:
                    # 文件已存在，继续下载
                    print("Continue download...")
                    self.__GetExistFile(filename, fileExistDIR, ftpDir) # 10线程 续传
                    return 0
        # 文件不存在，开始下载ts
        print("New download...")
        self.__GetNewFile(filename, fileExistDIR, ftpDir)

        return 0


class SelfFTP(FTP):
    def __init__(self, ftpInfo):
        super(SelfFTP, self).__init__(ftpInfo)
