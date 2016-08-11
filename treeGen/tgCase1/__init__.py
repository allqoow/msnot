#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : SoanNunim
# Contact   : 
# Started on: 20160725
# Project	: msnot

import re
class tgCase1():
	def __init__(self, ejlisedSen, taggedSen, db, cddCmpntList, cpTypeToken, sfGenerator):
		self.ejlisedSen = ejlisedSen #ejlisedSen=어절lized 문장
		self.taggedSen = taggedSen
		self.db = db
		self.cddCmpntList = cddCmpntList #candidatecomponentlist : 어디로 자를지 모를 때 앞에 있는 후보자들 리스트
		self.cpTypeToken = cpTypeToken
		self.sfGenerator = sfGenerator

		self.schemeIndex0 = 0
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = cddCmpntList
		self.schemeAnnex = {"case":"case1", "alias":"CompleteSentence"}

		yongeonPart = self.cddCmpntList[-1]
		self.sfGenerator.createSearchInputYongeon(yongeonPart)
		self.sfGenerator.getSemanticFeature()
		
		for x in self.cddCmpntList:
			if "NP" in x[2]:
				cheeonPart = x
				self.sfGenerator.createSearchInputCheeon(cheeonPart)
				self.sfGenerator.getSemanticFeature()
		self.process()

		self.process()

	def process(self):
		print "저는 Case1을 맡고 있습니다!!!!!"
		auxList2 = []
		self.schemeIndex0 = self.cddCmpntList[0][0]
		self.auxList2 = self.cddCmpntList