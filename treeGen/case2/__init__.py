#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160723(yyyymmdd)
# Project	: msnot

import re
class case2():
	def __init__(self, ejlisedSen, taggedSen, db, auxList1, cpTypeToken):
		print "저는 Case2를 맡고 있습니다!"		
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db
		self.auxList1 = auxList1
		self.cpTypeToken = cpTypeToken

		self.schemeIndex0 = 0
		self.schemeIndex1 = auxList1[-1][1]
		self.auxList2 = auxList1
		self.schemeAnnex = {}

		self.process()
		self.schemeAnnex["adjusted"] = True


	def process(self):
		for x in self.taggedSen:
			print x[0] + ' ' + str(x[1]) + '    ',
		print '\n'
		for x in self.ejlisedSen:
			print x[0] + ' ' + str(x[1]) + '   ',
		print '\n'
		print self.cpTypeToken

		self.testSemanticAvail()

		if self.semanticAvail == True:
			pass
		elif self.semanticAvail == False:
			print '+++++++++++testSemanticAvail==False+++++++++++'
			tList0 = [item[2] for item in self.auxList1]
			tList1 = [item[1] for item in self.taggedSen]
			
			countForTl1 = 0
			for x in tList1:
				if x in ["VA", "VV", "VX"]:
					countForTl1 += 0


		auxList2 = []	
		#self.schemeIndex0 = self.auxList1[0][0]
		#self.auxList2 = self.auxList1
		
	def testSemanticAvail(self):
		print '+++++++++++testSemanticAvail++++++++++++++++++'
		# some conditions e.g. there exists a db for sematic analysis
		if True==False:
			self.semanticAvail = True
		# otherwise
		else:
			self.semanticAvail = False