#!/usr/bin/env python3
# encoding: utf-8

import settings
from FtpInfo import FtpInfo
from Processor import ProcessorFactory
import os


class FTPFactory:
    def __init__(self, ftpInfo):
        if type(ftpInfo) is not FtpInfo:
            raise TypeError

        self.ftpInfo = ftpInfo

    def GetFTP(self):
        return LFTP(self.ftpInfo)


class FTP:
    """其实这应该是抽象类...WTF!!"""
    def __init__(self, ftpInfo):
        self.ftp = FTPFactory(ftpInfo).GetFTP()

    def GetList(self):
        print("Get list...")
        fileList = self.ftp.GetList()
        print("Got list.")

        return fileList

    def GetFile(self, filename, fileSize, downloadDIR=settings.Download_Dir):
        for cfile in os.listdir(downloadDIR):
            if filename.lower() == cfile.lower():
                if os.path.getsize(os.path.join(downloadDIR, filename)) >= int(fileSize):
                    # 文件已存在，下载已完成
                    print("Download end.")
                    return 2
                else:
                    # 文件已存在，继续下载
                    print("Continue download...")
                    self.ftp.GetExistFile(filename) # 10线程 续传
                    return 0
        # 文件不存在，开始下载ts
        print("New download...")
        self.ftp.GetNewFile(filename)
        return 0


class LFTP:
    def __init__(self, ftpInfo):
        if type(ftpInfo) is not FtpInfo:
            raise TypeError

        loginCM = settings.CM_ftp_Login.format(
                host   = ftpInfo['host'],
                user   = ftpInfo['user'],
                passwd = ftpInfo['passwd']
            )
        if ftpInfo['ssh'] == "TLS_V1" or ftpInfo['ssh'] == "SSL_V3":
            loginCM += settings.CM_ftp_Login_TLS_V1

        self.processor = ProcessorFactory(loginCM).GetProcessor()

    def GetList(self):
        self.processor(settings.CM_ts_List)

        try:
            with open(settings.LOG_Filename, encoding='utf-8') as logFile:
                return logFile.read()
        except FileNotFoundError:
            print("[IOError]: No such file or directory: {}".format(logFile))
            return ''

    def GetNewFile(self, filename, args=settings.ARGS_New_ts_Get):
        self.processor(settings.CM_LFTP_Get_File.format(args=args, filename=filename))

    def GetExistFile(self, filename, args=settings.ARGS_Continue_ts_Get):
        self.processor(settings.CM_LFTP_Get_File.format(args=args, filename=filename))


class SelfFTP:
    def __init__(self):
        pass
