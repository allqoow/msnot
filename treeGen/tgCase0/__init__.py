#!/usr/bin/python
# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
<<<<<<< HEAD
# Author    : cheukusi
# Contact   : cheukusi.kim@gmail.com
# Started on: 20160725
=======
# Author    : moon-eunseo
# Contact   : aristocat1703@gmail.com
# Started on: 20160725(yyyymmdd)
>>>>>>> bfe8310ff4b6ec5d9406c333c8bd979f595a8468
=======
# Author    : moon-eunseo
# Contact   : aristocat1703@gmail.com
# Started on: 20160725(yyyymmdd)
>>>>>>> bfe8310ff4b6ec5d9406c333c8bd979f595a8468
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
		print "저는 Case2을 맡고 있습니다!"
		auxList2 = []
		self.schemeIndex0 = self.cddCmpntList[0][0]
		self.auxList2 = self.cddCmpntList