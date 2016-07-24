#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : Your developer name
# Contact   : Your eMail
# Started on: 201607??(yyyymmdd)
# Project	: msnot

class case0():
	def __init__(self, ejlisedSen, taggedSen, db, auxList1, cpTypeToken):
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
	def process(self):
		print "저는 Case0을 맡고 있습니다!"
		auxList2 = []
		self.schemeIndex0 = self.auxList1[0][0]
		self.auxList2 = self.auxList1