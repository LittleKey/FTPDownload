#!/usr/bin/env python3
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
# 如果把lftp添加到了环境变量里应该连这个也不用设置了( 尚未测试
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
CM_Execute_Win32 = \
r"""@echo off
cd /d {LFTP_DIR}
set PYTHONIOENCODING=utf8
lftp -f "{CONF_Filename}" > "{LOG_Filename}"
""".format(LFTP_DIR=LFTP_DIR, CONF_Filename=basename(CONF_Filename), LOG_Filename=LOG_Filename)

CM_Execute_Linux = \
r"""
lftp -f "{CONF_Filename}" > "{LOG_Filename}"
""".format(CONF_Filename=basename(CONF_Filename), LOG_Filename=LOG_Filename)

# 指定ts下载目录的命令
CM_ts_Download_Dir = \
r"""
lcd {Download_Dir}
""".format(Download_Dir=Download_Dir)

# 获取ts文件列表的命令
CM_ts_List = \
r"""
ls -l
"""

# 获取ts文件的命令
CM_ts_Get = \
r"""
pget {args} {filename}
"""

# pget 续传文件的命令的参数
ARGS_Continue_ts_Get = r"-c -n 10"

# pget 新下载文件的命令的参数
ARGS_New_ts_Get = r"-n 10"

# lftp 下载文件命令
CM_LFTP_Get_File = CM_ts_Download_Dir + CM_ts_Get

# FTP登陆命令
CM_ftp_Login = \
r"""
lftp {host}
login {user} {passwd}
"""
# 登录TLS_V1验证FTP的设置
CM_ftp_Login_TLS_V1 = \
r"""
set ssl:verify-certificate no
"""
