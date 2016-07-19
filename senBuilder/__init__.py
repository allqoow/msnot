#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

# 구글번역기로 대체할 부분
# 4-2. rearranging & substituting to English words
# 4-3. reconstructing a sentence from a tree

class senBuilder():

	# reuse open driver
	def __init__(self, driver, ejlisedSen, schemeList, partialTransListExt):
		self.driver = driver 
		self.ejlisedSen = ejlisedSen
		self.schemeList = schemeList
		self.partialTransListExt = partialTransListExt 
		
		self.partialTransList = []
		self.schemeIndex = 0
		self.schemeAdjust = 0
		self.translatedOrder = 0
		self.cache0 = ''
		self.finalOutput = ''

		self.driver.get('https://translate.google.co.kr/?hl=ko#ko/en/')		
		while self.schemeIndex < len(self.schemeList):
			self.enterToSource()
		self.deAlias()

	def enterToSource(self):
		scheme = self.schemeList[self.schemeIndex]
		ejIndex0 = 0
		ejIndex1 = 0
		#print scheme
		for i in range(len(self.ejlisedSen)):
			if self.ejlisedSen[i][1][0] == scheme[0]:
				ejIndex0 = i 
			if self.ejlisedSen[i][1][1] == scheme[1]:
				ejIndex1 = i+1 

		#print ejIndex0
		#print ejIndex1

		inputPhrase = ''
		for x in self.ejlisedSen[ejIndex0:ejIndex1]:
			inputPhrase += str(x[0])
			inputPhrase += ' '
		print inputPhrase
		inputPhrase = unicode(inputPhrase.strip())
		self.driver.get('https://translate.google.co.kr/?hl=ko#ko/en/')
		elementSource = self.driver.find_element_by_id('source')
		elementSource.send_keys('')
		elementSource.send_keys(inputPhrase)

		# in case the engine runs too fast
		rawPartialTrans = ''
		while len(rawPartialTrans) < 5:
			elementResult = self.driver.find_element_by_id('result_box')
			rawPartialTrans = str(elementResult.text)
			if self.cache0 == rawPartialTrans:
				rawPartialTrans = ''
			print 'waiting for result'
		self.cache0 = rawPartialTrans
		print rawPartialTrans
		print '\n'
		#print self.schemeAdjust

		phrasePos = self.schemeList[self.schemeIndex][2]

		self.partialTransSave(ejIndex0, ejIndex1, rawPartialTrans, phrasePos)

		#self.schemeAdjust = scheme[1] - scheme[0] - 1
		self.schemeIndex += 1

	def partialTransSave(self, ejIndex0, ejIndex1, rawPartialTrans, phrasePos):
		# Case 1
		if phrasePos == 'MAG':
			alias = 'Then'
			#alias = 'Dann'
			#alias = 'entonces,'
		else:
			alias = 'CompleteSentence'

		self.partialTransList.append([rawPartialTrans, alias, self.translatedOrder])
		self.enAlias(ejIndex0, ejIndex1, alias)

		self.translatedOrder += 1
		print self.partialTransList
		print '\n'

	def enAlias(self, ejIndex0, ejIndex1, alias):
		self.ejlisedSen[ejIndex0][0] = alias
		for i in range(ejIndex0+1, ejIndex1):
			self.ejlisedSen[i][0] = ''	
		
		print self.ejlisedSen

	def deAlias(self):
		self.cache0 = ''
		#aa = self.partialTransList.reverse()
		#for i in range(len(aa)):
		#	self.cache0 = x[0]
		for i in range(self.translatedOrder-1,-1,-1):
			for x in self.partialTransList:
				if i == x[2]:
					print x[1]
					if x[1] == 'CompleteSentence':
						self.cache0 = x[0]
					else:
						print x[1]
						print x[0]
						self.cache0 = self.cache0.replace(x[1], x[0])
		self.finalOutput = self.cache0
		print self.cache0


