#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160727(yyyymmdd)
# Project	: msnot
import re
class tgCase20():
	def __init__(self, ejlisedSen, taggedSen, db, cddCmpntList, cpTypeToken):
		print '_____Below is the place for your logs(Case20)_____\n\n'
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db
		self.cddCmpntList = cddCmpntList
		self.cpTypeToken = cpTypeToken

		self.schemeIndex0 = self.cddCmpntList[-1:][0][0]
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = self.cddCmpntList[-1:]
		self.schemeAnnex = {"case":"case2", "alias":"CompleteSentence"}

		self.process()
		print '_____Above is the place for your logs(Case20)_____\n\n'

	def process(self):
		if self.taggedSen[self.schemeIndex0][1] == "VV":
			toPhrFix = str(self.taggedSen[self.schemeIndex0][0])
			toPhrFix = str(toPhrFix + "다")
			if "phrFix" not in self.schemeAnnex:
				self.schemeAnnex["phrFix"] = []
			self.schemeAnnex["phrFix"].append([toPhrFix, [5,7]])

		print "저는 Case20을 맡고 있습니다!"
		print self.schemeIndex0
		print self.schemeIndex1
		print self.cfmdCmpntList
		print self.schemeAnnex