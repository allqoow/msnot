#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

class corpusTagger:
	"""
	=== Module for Stage 2 ===
	"""
	def __init__(self, rawSenList):
		self.rawSenList = rawSenList
		self.taggedSenList = []
		self.ejlisedSenList = []
	def taggingWithKomoran(self):
		from konlpy.tag import Komoran
		Komoran = Komoran()
		for x in self.rawSenList:
			# ejlisedSen
			a = Komoran.pos(x,False)
			ejlisedSen = x.split()
			pointer = 0
			for i in range(len(a)):
				ejIndex = [pointer, pointer + len(a[i])]
				ejlisedSen[i] = [ejlisedSen[i], ejIndex]
				pointer = pointer + len(a[i])
			self.ejlisedSenList.append(ejlisedSen)
			
			# taggedSen
			b = Komoran.pos(x)
			self.taggedSenList.append(b)

	def taggingWithKkma(self):
		from konlpy.tag import Kkma
		Kkma = Kkma()
		for x in self.rawSenList:
			b = Kkma.pos(x)
			self.taggedSenList.append(b)

	def taggingWithUCorpus(self):
		"""
		driver = webdriver.Firefox()
		driver.get('http://203.250.77.84')
		inputBox = driver.find_element_by_id('TextBox1')
		inputBox.send_keys(b)
		outputBox = driver.find_element_by_id('TextBox2').text
		outputBox = str(outputBox)
		cc = outputBox.split('★')
		"""
		pass