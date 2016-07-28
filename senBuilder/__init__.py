#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

class senBuilder():

	# reuse open driver
	def __init__(self, driver, ejlisedSen, schemeList, schemeAnnexList, partialTransListExt):
		self.driver = driver 
		self.ejlisedSen = ejlisedSen
		self.schemeList = schemeList
		self.schemeAnnexList = schemeAnnexList
		self.partialTransListExt = partialTransListExt 
		
		self.inputPhrase = ''
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

		self.inputPhraseGen(ejIndex0, ejIndex1)

		# specific to google.translate
		self.driver.get('https://translate.google.co.kr/?hl=ko#ko/en/')
		elementSource = self.driver.find_element_by_id('source')
		elementSource.send_keys('')
		elementSource.send_keys(self.inputPhrase)

		# in case the engine runs too fast
		rawPartialTrans = ''
		print 'waiting for result'
		while len(rawPartialTrans) < 5:
			elementResult = self.driver.find_element_by_id('result_box')
			rawPartialTrans = str(elementResult.text)
			if self.cache0 == rawPartialTrans:
				rawPartialTrans = ''
			#print 'waiting for result'
		self.cache0 = rawPartialTrans
		print rawPartialTrans
		print '\n'
		#print self.schemeAdjust

		phrasePos = self.schemeList[self.schemeIndex][2]

		if "rtsrFlag" in self.schemeAnnexList[self.schemeIndex]:
			self.partialTransList.append([rawPartialTrans, alias, self.translatedOrder])
			self.enAlias(ejIndex0, ejIndex1, alias)
			self.translatedOrder += 1
			pass
		else:
			self.partialTransSaveRegular(ejIndex0, ejIndex1, rawPartialTrans, phrasePos)
		#self.schemeAdjust = scheme[1] - scheme[0] - 1
		self.schemeIndex += 1

	def inputPhraseGen(self, ejIndex0, ejIndex1):
		"""
		if self.schemeAnnexList[self.schemeIndex]["case"] == "case0":
			pass
		elif self.schemeAnnexList[self.schemeIndex]["case"] == "case1":
			pass
		elif self.schemeAnnexList[self.schemeIndex]["case"] == "case2":
			pass
			#from sbCase0 import sbCase0
		"""
		inputPhrase = ''
		# 구절 자체를 손대야 하는 경우 여기서
		for x in self.ejlisedSen[ejIndex0:ejIndex1]:
			if "phrFix" in self.schemeAnnexList[self.schemeIndex]:
				for y in self.schemeAnnexList[self.schemeIndex]["phrFix"]:
					if x[1] == y[1]:#??
						x[0] = y[0]
						break

			print str(x[0])
			inputPhrase += str(x[0])
			inputPhrase += ' '

		# 전 시행에서 첨부된 부분 삭제(바로 전 시행만 해도 괜찮을까?)
		if "phrAppend" in self.schemeAnnexList[self.schemeIndex-1]:
		# ISSUE: replace only first match
			inputPhrase = inputPhrase.replace(self.schemeAnnexList[self.schemeIndex-1]["phrAppend"][0], '')

		# 주로 수식대상이 관련되지 않을까?
		if "phrAppend" in self.schemeAnnexList[self.schemeIndex]:
			inputPhraseAppend = self.schemeAnnexList[self.schemeIndex]["phrAppend"][0]
		else:
			inputPhraseAppend = ''
		
		# 주로 추정된 주어가 아닐까?
		if "phrPrepend" in self.schemeAnnexList[self.schemeIndex]:
			inputPhrasePrepend = self.schemeAnnexList[self.schemeIndex]["phrPrepand"]#[0]
		else:
			inputPhrasePrepend = ''

		print inputPhrasePrepend
		print inputPhrase	
		print inputPhraseAppend
		inputPhrase = inputPhrasePrepend + inputPhrase + inputPhraseAppend
		inputPhrase = unicode(inputPhrase.strip())
		self.inputPhrase = inputPhrase


	def partialTransSaveRegular(self, ejIndex0, ejIndex1, rawPartialTrans, phrasePos):
		# Case 1
		alias = self.schemeAnnexList[self.schemeIndex]["alias"]
		"""
		if self.schemeAnnexList[self.schemeIndex]["case"] == "case0":
			pass
		elif self.schemeAnnexList[self.schemeIndex]["case"] == "case1":
			pass
		elif self.schemeAnnexList[self.schemeIndex]["case"] == "case2":
			alias = self.schemeAnnexList[self.schemeIndex]["case"]
		"""
			
			#alias = 'Dann'
			#alias = 'entonces,'

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