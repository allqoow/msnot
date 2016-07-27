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

		self.schemeIndex0 = 0
		self.schemeIndex1 = cddCmpntList[-1][1]
		self.cfmdCmpntList = cddCmpntList
		self.schemeAnnex = {"case":"case2", "alias":"CompleteSentence"}

		self.process()
		print '_____Below is the place for your logs(Case20)_____\n\n'

	def process(self):
		print "저는 Case20을 맡고 있습니다!"