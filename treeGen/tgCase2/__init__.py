#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : Gomyul
# Contact   : ldh2051@gmail.com
# Started on: 201607??(yyyymmdd)
# Project	: msnot


import re


class tgCase2():
	def __init__(self, ejlisedSen, taggedSen, db, cddCmpntList, cpTypeToken, sfGenerator):
		# input needed for generating this class
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db
		self.cddCmpntList = cddCmpntList
		self.cpTypeToken = cpTypeToken
		self.sfGenerator = sfGenerator

		# output needed to be generated from class
		self.schemeIndex0 = 0
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = cddCmpntList
		self.schemeAnnex = {"case":"case2", "alias":"CompleteSentence"}

		# process
		print "저는 Case2를 맡고 있습니다!"
		yongeonPart = self.cddCmpntList[-1]
		self.sfGenerator.createSearchInputYongeon(yongeonPart)
		self.sfGenerator.getSemanticFeature()
		
		for x in self.cddCmpntList:
			if "NP" in x[2]:
				cheeonPart = x
				self.sfGenerator.createSearchInputCheeon(cheeonPart)
				self.sfGenerator.getSemanticFeature()
		self.process()

	def process(self):
		#self.semanticAnalysis = True
		self.semanticAnalysis = False
		if self.semanticAnalysis == False:
			print '+++++++++++testSemanticAvail==False+++++++++++'
			tList0 = [item[2] for item in self.cddCmpntList]
			for x in tList0:
				if x in ['NP_SBJ', 'NP_OBJ']:
					singleSyllableVp = False
				else:
					singleSyllableVp = True

			if self.cddCmpntList[-1][1] - self.cddCmpntList[-1][0] == 2 and singleSyllableVp == True:
				from tgCase20 import tgCase20
				case20 = tgCase20(self.ejlisedSen, self.taggedSen, self.db, self.cddCmpntList, self.cpTypeToken)
				self.schemeIndex0 = case20.schemeIndex0
				self.schemeIndex1 = case20.schemeIndex1
				self.cfmdCmpntList = case20.cfmdCmpntList
				self.schemeAnnex = case20.schemeAnnex
			else:
				tList0 = [item[2] for item in self.cddCmpntList]
				tList1 = [item[1] for item in self.taggedSen]
				
				countForTl0 = 0
				cutGuide0 = []
				for i in range(len(tList0)):
					if tList0[i] == "NP_SBJ":
						countForTl0 += 1
						cutGuide0.append(i)
				print countForTl0
				print cutGuide0

				if countForTl0 == 0:
					#목적어가 없다면
					self.schemeIndex0 = self.cddCmpntList[-1][0]
					print self.schemeIndex0
				elif countForTl0 == 1:
					#목적어가 없다면
					#cutGuide1 = self.cddCmpntList[cutGuide0][0]
					#print cutGuide1
					#self.schemeIndex0 = cutGuide1
					self.schemeIndex0 = self.cddCmpntList[cutGuide0[0]][0]
				elif countForTl0 > 1:
					self.schemeIndex0 = self.cddCmpntList[cutGuide0[-1]][0]
					pass

				countForTl1 = 0
				for x in tList1:
					if x in ["VA", "VV", "VX"]:
						countForTl1 += 0
						self.schemeAnnex["adjusted"] = True
				print countForTl1

				# 동사 단독구면 확실히 다른 처리를 해야 한다.

				# 어떤 명사를 수식하는지 보자.
				# 필요에 따라서는 추가까지
				print '+++++++++++어떤 명사를 수식하는지 보자+++++++++++++++'
				appendGuide0 = self.cddCmpntList[-1][1]
				for x in self.ejlisedSen:
					if x[1][0] == appendGuide0:
						appendGuide1 = x[1][1]

						print appendGuide0
						print appendGuide1
						"""
						for y in self.taggedSen[appendGuide0:appendGuide1]:
							if y[0] in ["동안","때","도중","중간"]:
								self.schemeAnnex["phrAppend"] = x
								self.schemeAnnex["alias"] = "sometime"
						break
						"""
						for y in self.taggedSen[appendGuide0:appendGuide1]:
							if y[0] in ["곳","장소","식당"]:
								self.schemeAnnex["phrAppend"] = x
								self.schemeAnnex["alias"] = "somewhere"
						break		
				"""
				# temporal noun(?)
				phraseAppendCddList0 = ['동안','때','도중']
				print self.taggedSen[appendGuide0][0]
				
				
				
				else:
					for x in self.ejlisedSen:
						if x[1][0] == appendGuide0:
							print x[0]
							print x[1][0]
							print x[1][1]
							self.schemeAnnex["phrAppend"] = x
							self.schemeAnnex["alias"] = "something"
				"""

				print self.schemeAnnex