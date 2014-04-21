#!/usr/bin/env python
#encoding: utf-8

################
#			   #
# 各种全局变量 #
#			   #
################

from os.path import basename
from os.path import abspath
from os.path import join
from os.path import exists

# lftp所在的目录(必填, 后面的设置可以不改动)
LFTP_DIR = abspath(r'C:\cygwin\bin')

#======================================================================================#
# FTP 信息(host, user, passwd)....请妥善保管...
FTP_Conf_File = abspath(r'ac.conf')
FTP_Conf_File = exists(FTP_Conf_File) and FTP_Conf_File or ''

# ts下载目录 [default: 程序所在目录]
Download_Dir = abspath(r'.')

# ts list (伪)Log文件的输出地址
LOG_Filename = abspath(r'./tsList.log')
# ftp配置文件的输出地址
CONF_Filename = abspath(join(LFTP_DIR, r'_lftp.conf'))


# 以下各种命令，请勿随意改动
#======================================================================================#
# 处理各种命令的脚本
CM_Execute = \
r"""@echo off
cd /d {LFTP_DIR}
set PYTHONIOENCODING=utf8
lftp -f "{CONF_Filename}" > "{LOG_Filename}"
""".format(LFTP_DIR=LFTP_DIR, CONF_Filename=basename(CONF_Filename), LOG_Filename=LOG_Filename)

def ProcessorFactory():
    pass
