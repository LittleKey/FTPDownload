#!/usr/bin/env python
# encoding: utf-8

import settings


# 指定ts下载目录的命令
CM_ts_Download_Dir = \
r"""
lcd {Download_Dir}
""".format(Download_Dir=settings.Download_Dir)

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

# FTP登陆命令
CM_ftp_Login = \
r"""
lftp {host}
login {user} {passwd}
"""
# 登录TLS_V1验证FTP的设置
CM_ftp_Login_TLS_V1 = \
r"""
set ssl::verify-certificate no
"""

class LFTP:
    def __init__(self):
        pass

