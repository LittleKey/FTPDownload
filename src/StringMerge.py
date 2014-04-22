#!/usr/bin/env python3
#encoding: utf-8

##############################
#			                 #
#  我有特别的字符串合成技巧  #
#			                 #
##############################

class StringMerge:
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

