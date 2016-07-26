#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : moon-eunseo
# Contact   : aristocat1703@gmail.com
# Started on: 20160725(yyyymmdd)
# Project	: msnot

import re
class tgCase0():
	def __init__(self, ejlisedSen, taggedSen, db, cddCmpntList, cpTypeToken):
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db
		self.cddCmpntList = cddCmpntList
		self.cpTypeToken = cpTypeToken

		self.schemeIndex0 = 0
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = cddCmpntList
		self.schemeAnnex = {"case":"case0", "alias":"CompleteSentence"}

		self.process()
	def process(self):
		print "저는 Case0을 맡고 있습니다!"
		for x in self.taggedSen:
			print x[0] + ' ' + str(x[1]) + '    ',
		print '\n'
		for x in self.ejlisedSen:
			print x[0] + ' ' + str(x[1]) + '   ',
		print '\n'
		print self.cddCmpntList
		print self.cpTypeToken
<<<<<<< HEAD

		auxList2 = []
		self.schemeIndex0 = self.cddCmpntList[0][0]
		self.auxList2 = self.cddCmpntList

=======
		
		auxList2 = []
		self.schemeIndex0 = self.cddCmpntList[0][0]
		self.auxList2 = self.cddCmpntList
>>>>>>> origin/master
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
<<<<<<< HEAD
=======

>>>>>>> origin/master
		"""
