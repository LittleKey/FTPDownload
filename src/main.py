#!/usr/bin/env python3
#encoding: utf-8

################
#			   #
#     本体     #
#			   #
################

__Author__ = 'LittleKey'
__Version__ = '1.0'
__doc__ = \
"""
FTP downloader
"""

import os
from subprocess import call
import re
from Filename import Filename
import settings
from getpass import getpass


def MoveFile(cFilename, tFilename):
	# 这已经没用了
	pass

def AnimeMatch(animeName, context): #如果有匹配到ts则返回[(大小, 集数,  电视台),...]。
	# 暂时只是为了剑灵之类ts写的正则表达式, 因为要使用format，所以请勿使用 '{}'
	match = re.compile(r'group   (\d.*) \w+\w+\w+.*? {}_?(\d*)_?(.*?)\.ts'.format(animeName.strip()), \
																						re.IGNORECASE)
	matchList = match.findall(context)
	#print(matchList)
	return matchList

def LastAnimeGet(animeName, TV, context): # 获取最新一集的ts
	if TV:
		# 按电视台和集数，从小到大升序排序
		rlt = sorted(AnimeMatch(animeName, context), key=lambda t: t[1] and t[2].upper() == TV.upper())
	else:
		# 按集数，从小到大升序排序
		rlt = sorted(AnimeMatch(animeName, context), key=lambda t: t[1])

	if rlt:
		#print(rlt[-1])
		return rlt[-1] # 最后一个集数最大
	else:
		#print(rlt)
		print("No Match.")
		return False

def Clear(*args):
	# 清理文件
	for aFile in args:
		try:
			os.remove(aFile)
		except FileNotFoundError:
			print("No such file {}".format(aFile))
		except NotImplementedError:
			print("Your platform not support remove.")
			return -1


class FTP:
	def __init__(self, host, user, password, CM_Login=settings.CM_ftp_Login, CM_Execute=settings.CM_Execute):
		self.host = host
		self.user = user
		self.password = password

		self.Processor = self.__ExecuteCommand(CM_Execute) # 配置文件处理器
		self.CM = self.__Connect(CM_Login) # 登陆命令

	def TSList(self, CM=settings.CM_ts_List, CM_Filename=settings.CONF_Filename, LOG_Filename=settings.LOG_Filename):
		with open(CM_Filename, 'w') as outputFile:
			outputFile.write(self.CM)
			outputFile.write(CM)

		self.Processor()
		try:
			with open(LOG_Filename, encoding='utf-8') as logFile:
				return logFile.read()
		except FileNotFoundError:
			print("[IOError]: No such file or directory: {}".format(logFile))

        return ''

	def __Connect(self, CM_Login): # 待优化

		return CM_Login.format(host=self.host, user=self.user, passwd=self.password)

	def __ExecuteCommand(self, CM_Execute):
		self.filename = r"w@i@n@dr@a@i@n.cmd"
		if not os.path.exists(self.filename):
			with open(self.filename, 'w') as wrFile:
				wrFile.write(CM_Execute)

		return self.__Call

	def __Call(self):

		call([self.filename])


	def TSGet(self, filename, \
			  args, \
			  CM=settings.CM_ts_Get, CM_Filename=settings.CONF_Filename):

		with open(CM_Filename, 'w') as outputFile:
			outputFile.write(self.CM)
			outputFile.write(settings.CM_ts_Download_Dir) # 设置下载目录，需要放在下载命令前
			outputFile.write(CM.format(args=args, filename=filename))

		print("Download start...")
		self.Processor()
		print("Download end.")

def GetTSList(ftp):
	print("Get ts list...")
	tsList = ftp.TSList()
	print("Got it.")

	return tsList

def DownloadTS(ftp, filename, size, Download_DIR=settings.Download_Dir):
	for cfile in os.listdir(Download_DIR):
		if filename.lower() == cfile.lower():
			if os.path.getsize(os.path.join(Download_DIR, filename)) >= int(size):
				# 文件已存在，下载已完成
				print("Download Finish.")
				return 2
			else:
				# 文件已存在，继续下载
				print("Continue download.")
				ftp.TSGet(filename, settings.ARGS_Continue_ts_Get) # 10线程 续传
				return 1
	# 文件不存在，开始下载ts
	print("New Dowaload.")
	ftp.TSGet(filename, settings.ARGS_New_ts_Get)
	return 0

def GetFTPInfo(ftpConf):
	try:
		# 从配置文件获取
		with open(ftpConf) as ACFile:
			host = ACFile.readline().strip()
			account = ACFile.readline().strip()
			password = ACFile.readline().strip()
	except FileNotFoundError:
		# 如果没有配置文件，则改为手动输入
		host = input("host: ")
		account = input("account: ")
		password = getpass("password: ")

	return host, account, password

def main(animeName, lastNum=0, STV='', ftpConf=settings.FTP_Conf_File):
	host, account, password = GetFTPInfo(ftpConf)

	ftp = FTP(host, account, password)

	#animeName = r'blade_and_soul'

	tsList = GetTSList(ftp)
	try:
		size, num, TV = LastAnimeGet(animeName, STV, tsList) # 获取最新一集动画的集数与大小
		if STV != '' and STV.upper() != TV.upper():
			#print(STV + ' ' + TV)
			raise TypeError
		#print("{}, {}, {}, {}".format(size, num, TV, filename))
	except TypeError:
		print("{} {} 尚未更新，5分钟后再次检查...".format(animeName, STV))
		return -1

	if lastNum != 0 and int(num) < lastNum: # 限制只下多少集之后的ts
		print("{} {} 第{}集 尚未更新，5分钟后再次检查...".format(animeName, TV, lastNum))
		return -1

	filename = Filename(head=animeName, foot='.ts', middleWare='_', stringList=[num, TV]).Return() # EP

	print(r"{} size: {}".format(filename, size))

	return DownloadTS(ftp, filename, int(size))



if __name__ == '__main__':
	main(r'blade_and_soul')
	#main(r'Chu22')
	input()
