#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : Your developer name
# Contact   : Your eMail
# Started on: 201607??(yyyymmdd)
# Project	: msnot


import re
class tgCase2():
	def __init__(self, ejlisedSen, taggedSen, db, cddCmpntList, cpTypeToken):
		print "저는 Case2를 맡고 있습니다!"		
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db
		self.cddCmpntList = cddCmpntList
		self.cpTypeToken = cpTypeToken

		self.schemeIndex0 = 0
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = cddCmpntList
		self.schemeAnnex = {"case":"case2", "alias":"CompleteSentence"}

		self.process()
		
	def process(self):
		for x in self.taggedSen:
			print x[0] + ' ' + str(x[1]) + '    ',
		print '\n'
		for x in self.ejlisedSen:
			print x[0] + ' ' + str(x[1]) + '   ',
		print '\n'
		print self.cddCmpntList
		print self.cpTypeToken

		self.testSemanticAvail()

		if self.semanticAvail == True:
			pass
		elif self.semanticAvail == False:
			if self.cddCmpntList[-1][1] - self.cddCmpntList[-1][1] == 2:
				#from tgCase00 import tgCase00
				#case00 = tgCase00()
				#self.schemeIndex0 = case00.schemeIndex0
				#self.schemeIndex1 = case00.schemeIndex1
				#self.cfmdCmpntList = case00.cfmdCmpntList
				#self.schemeAnnex = case00.schemeAnnex
			else:
				print '+++++++++++testSemanticAvail==False+++++++++++'
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


	def testSemanticAvail(self):
		print '+++++++++++testSemanticAvail++++++++++++++++++'
		# some conditions e.g. there exists a db for semantic analysis
		if True == False:
			self.semanticAvail = True
		# otherwise
		else:
			self.semanticAvail = False