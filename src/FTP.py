#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import settings
from FtpInfo import FtpInfo
from Processor import ProcessorFactory
import os
from subprocess import call
from sys import stdout


class FTPFactory:
    def __init__(self, ftpInfo=FtpInfo()):
        if not isinstance(ftpInfo, FtpInfo):
            raise TypeError

        self.ftpInfo = ftpInfo
        self.ftpInfo.GetInfo()

    def GetFTP(self):
        # 暂时只有这一个FTP实现，所以这样写了...
        try:
            print("Get lftp version...\n")
            call([os.path.join(settings.LFTP_DIR, 'lftp'), '--version'])
            return LFTP(self.ftpInfo)
        except IOError:
            print("[IOError]: No found lftp")
            exit(0)
        finally:
            print("\n")



class FTP:
    """其实这应该是抽象类...WTF!!"""
    def __init__(self, ftpInfo):
        if not isinstance(ftpInfo, FtpInfo):
            raise TypeError
        self.ftpInfo = ftpInfo

    def GetList(self, fileListDir):
        raise NotImplementedError

    def GetFile(self, filename, filesize, downloadDIR):
        raise NotImplementedError


class LFTP(FTP):
    r"""使用processor来处理各种lftp命令"""
    def __init__(self, ftpInfo):
        super(LFTP, self).__init__(ftpInfo)

        self.processor = self.__SetProcessor(ftpInfo)

    def __SetProcessor(self,ftpInfo):
        loginCM = self.__GetLoginCM(ftpInfo)

        return ProcessorFactory(loginCM).GetProcessor()

    def __GetLoginCM(self, ftpInfo):
        loginCM = settings.CM_ftp_Login.format(
                host   = ftpInfo['host'],
                user   = ftpInfo['user'],
                passwd = ftpInfo['passwd']
            )
        if ftpInfo['ssh'].upper() == "TLS_V1" or ftpInfo['ssh'].upper() == "SSL_V3":
            loginCM += settings.CM_ftp_Login_TLS_V1  # 添加TLS_V1验证设置。。。

        return loginCM

    def GetList(self, fileListDir):
        print("Get list...", end='')
        stdout.flush()
        self.processor(settings.CM_ts_List.format(Dir=fileListDir))
        print("\r" + " "*len("Get list...") + "\r", end='')
        print("Got list.", end='\n\n')

        try:
            with open(settings.LOG_Filename, encoding='utf-8') as logFile:
                return logFile.read()
        except IOError:
            print("[IOError]: No such file or directory: {}".format(settings.LOG_Filename))
            return ''

    def __GetNewFile(self, filename, downloadDIR, ftpDir):
        args = settings.ARGS_New_ts_Get
        filename = os.path.join(ftpDir, filename)
        self.processor(settings.CM_LFTP_Get_File.format(Download_Dir=downloadDIR, args=args, filename=filename))

    def __GetExistFile(self, filename, downloadDIR, ftpDir):
        args = settings.ARGS_Continue_ts_Get
        filename = os.path.join(ftpDir, filename)
        self.processor(settings.CM_LFTP_Get_File.format(Download_Dir=downloadDIR, args=args, filename=filename))

    def GetFile(self, filename, filesize, downloadDIR, ftpDir):
        for cfile in os.listdir(downloadDIR):
            if filename.lower() == cfile.lower():
                if os.path.getsize(os.path.join(downloadDIR, filename)) >= int(filesize):
                    # 文件已存在，下载已完成
                    print("Download end.", end='\n\n')
                    return 2
                else:
                    # 文件已存在，继续下载
                    print("Continue download...")
                    self.__GetExistFile(filename, downloadDIR, ftpDir) # 10线程 续传
                    return 0
        # 文件不存在，开始下载ts
        print("New download...")
        self.__GetNewFile(filename, downloadDIR, ftpDir)

        return 0


class SelfFTP(FTP):
    def __init__(self, ftpInfo):
        super(SelfFTP, self).__init__(ftpInfo)
