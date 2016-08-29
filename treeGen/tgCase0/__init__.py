#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : moon-eunseo
# Contact   : aristocat1703@gmail.com
# Started on: 20160725(yyyymmdd)
# Project	: msnot

import re
class tgCase0():
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
		self.schemeAnnex = {"case":"case0", "alias":"CompleteSentence"}

		# process
		print "저는 Case0을 맡고 있습니다!"
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
		for x in self.taggedSen:
			print x[0] + ' ' + str(x[1]) + '    ',
		print '\n'
		for x in self.ejlisedSen:
			print x[0] + ' ' + str(x[1]) + '   ',
		print '\n'
		print self.cddCmpntList
		print self.cpTypeToken

		# clause ends with SF(comma)
		if self.cpTypeToken[1][1] in ["SF","SP"]:
			ecIndex = self.cddCmpntList[-1][1] -2
		# clause ends with EC
		#elif self.cpTypeToken[1][1] == "EC":
		else:
			ecIndex = self.cddCmpntList[-1][1] -1

		print self.taggedSen[ecIndex][0]
		# EC
		# 나열
		if self.taggedSen[ecIndex][0] in ["고","으며","면서","는다는지","다든가","든가"]:
			self.schemeAnnex["alias"] = "Then,"
		# 대립
		elif self.taggedSen[ecIndex][0] in ["으나","거니","다는데","디","데도","는데도","고도"]:
			self.schemeAnnex["alias"] = "However,"
		# ECS
		# 인과
		elif self.taggedSen[ecIndex][0] in ["아서","어서","므로","기에","으니","니까","는지라",
											"더니","느라고","는즉","길래","거늘","건데","고서는",
											"고서야","길래","자마자","으므로","므로","어서는","어선",
											"은바","어","어다가","라서","으므로서","으므로써","으니까","으니"]:
			self.schemeAnnex["alias"] = "Therefore"
		# 여기는 그냥 노가다 			
		



		"""
		#print '+++++++++++++++caseFlag0Gen+++++++++++++++++++'
		self.caseFlag0 = ''
		#auxList = []
		for k in self.treekeyList[i:i+2]:
			if k[1] == 'EC' and k[2] in ['고','지만','든지']:#등등
				#auxList.append('ECC')
				self.caseFlag0 = self.caseFlag0 + 'P'
			else:
				#auxList.append('ECS')
				self.caseFlag0 = self.caseFlag0 + 'S'
		#if len(auxList) == 1:
		#	self.caseFlag0 = auxList[0][-1]
		#else:
		#	self.caseFlag0 = auxList[0][-1] + auxList[1][-1]
		"""
		"""
		cfmdCmpntList = []
			# VP *
			if caseFlag10 == 0:
				schemeIndex0 = cddCmpntList[0][0]
				cfmdCmpntList = cddCmpntList
			elif caseFlag0 == 'S':
				schemeIndex0 = cddCmpntList[0][0]
				cfmdCmpntList = cddCmpntList
			# 대등 then 대등/ 대등
			elif caseFlag0 == 'PP' or caseFlag0 == 'P':
				schemeIndex0 = cddCmpntList[0][0]
				cfmdCmpntList = cddCmpntList
			# 대등 then 종속
			elif caseFlag0 =='PS':
				schemeIndex0 = cddCmpntList[0][0]
				cfmdCmpntList = cddCmpntList
			# 종속 then 대등
			elif caseFlag0 =='SP':
				# NP_SBJ VP NP_SBJ NP_SBJ VP
				if caseFlag11 == 2:# caseFlag11 >= 2
					schemeIndex0 = cddCmpntList[0][0]
					cfmdCmpntList = cddCmpntList
				elif caseFlag11 == 1 or caseFlag11 == 0:
					if caseFlag10 == 1:
						schemeIndex0 = cddCmpntList[0][0]
						cfmdCmpntList = cddCmpntList
					elif caseFlag10 == 2 or caseFlag10 == 3:
						for i in range(len(cddCmpntList)):
							if cddCmpntList[i][2] == 'NP_SBJ':
								schemeIndex0 = cddCmpntList[i+1][0]
								cfmdCmpntList = cddCmpntList[i+1:]
								break
			# 종속 then 종속
			elif caseFlag0 =='SS':
				# NP_SBJ VP NP_SBJ NP_SBJ VP
				if caseFlag11 == 2:# caseFlag11 >= 2
					schemeIndex0 = cddCmpntList[0][0]
					cfmdCmpntList = cddCmpntList
				elif caseFlag11 == 1 or caseFlag11 == 0:
					if caseFlag10 == 1:
						schemeIndex0 = cddCmpntList[0][0]
						cfmdCmpntList = cddCmpntList
					elif caseFlag10 == 2 or caseFlag10 == 3:
						for i in range(len(cddCmpntList)):
							if cddCmpntList[i][2] == 'NP_SBJ':
								schemeIndex0 = cddCmpntList[i+1][0]
								cfmdCmpntList = cddCmpntList[i+1:]
								break

		"""
