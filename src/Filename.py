#!/usr/bin/env python3
#encode: utf-8

##############################
#			                 #
#  我有特别的文件名合成技巧  #
#			                 #
##############################

class Filename:
	def __init__(self, head='', foot='', middleWare='', stringList=[]):
		r"""if middleWare is '_', output: head_string1_string2..._stringNfoot""" 
		self.out = head
		self.middleWare = middleWare

		for string in stringList:
			self.__MiddleWare(string)

		self.out += foot

	def __MiddleWare(self, string):	
		if string != '':
			self.out += self.middleWare + string

	def Return(self):
		return self.out


if __name__ == '__main__':
	print(Filename(head='blade_and_soul', foot='.ts', middleWare='_', stringList=['01', 'TBS']).Return())
	input()