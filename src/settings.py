#!/usr/bin/env python
#encoding: utf-8

################
#			   #
# 各种全局变量 #
#			   #
################

from __future__ import print_function
from os.path import basename
from os.path import abspath
from os.path import join
from os.path import exists
import platform
from os import environ

# lftp所在的目录(必填, 后面的设置可以不改动)
# 如果把lftp添加到了环境变量里就可以设置为‘’(空字符cd )
LFTP_DIR = abspath(r'')
if not exists(LFTP_DIR):
    print("[IOError]: No found 'lftp'")
    exit(0)

#======================================================================================#
# FTP 信息(host, user, passwd[, ssh])....请妥善保管...
# 这是可选设置，如果没有找到设置文件 则会要求(从标准输入)手动输入
FTP_Conf_File = abspath(r'ftpinfo.json')
FTP_Conf_File = exists(FTP_Conf_File) and FTP_Conf_File or ''

# 文件下载目录 [default: 执行程序所在目录]
Download_Dir = abspath(r'.')

# lftp命令文件
LFTP_CM_File = \
{
    "CM_ts_List": "\nrecls -1sB --block-size=1 --filesize \"{Dir}\"\n",
    "CM_queue": "\nqueue\n{Other_CM}\nqueue start\n",
    "CM_ftp_Login": "\nlftp \"{host}\"\nlogin \"{user}\" \"{passwd}\"\n",
    "CM_ftp_Login_TLS_V1": "\nset ssl:verify-certificate no\n",
    "CM_LFTP_Get_File": "\nlcd \"{Download_Dir}\"\npget {args} \"{filename}\"\n",
    "ARGS_Continue_ts_Get": "-c -n 10",
    "ARGS_New_ts_Get": "-n 10"
}