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
		print "저는 진지합니다."
		print "ㅖㅣㅖ"
		auxList2 = []
		self.schemeIndex0 = self.cddCmpntList[0][0]
		self.auxList2 = self.cddCmpntList