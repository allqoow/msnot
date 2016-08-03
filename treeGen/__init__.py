#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

class treeGen():
	def __init__(self, ejlisedSen, taggedSen, db):
		self.case = 0
		self.ejlisedSen = ejlisedSen
		self.taggedSen = taggedSen
		self.db = db

		self.treekeyList = []
		self.schemeList = []
		self.schemeAnnexList = []

		self.adjustExt = 0
		self.tagToCmpnt = []
		self.cmpntToCmpnt = []
		self.ttcPrevious = []
		self.adjustExt = 0
		self.auxListForCf1g = []

		self.treekeyListGen()
		self.schemeListGen()

	def treekeyListGen(self):
		print '++++++++++++++treekeyListGen++++++++++++++++++'
		# ISSUE: 콤마 등 문장부호 처리
		self.treekeyList = []
		for i in range(len(self.taggedSen)):
			if self.taggedSen[i][1] in ['EC','SF','ETN','ETM']:
				addInfo0 = str(self.taggedSen[i][1])
				addInfo1 = str(self.taggedSen[i][0])
				self.treekeyList.append([i, addInfo0, addInfo1])
		print self.treekeyList

		# 보조용언이 붙은 경우 제거
		invalidTreekeyList0 = []
		for x in self.treekeyList:
			try: 
				if self.taggedSen[x[0]+1][1] == 'VX':
					invalidTreekeyList0.append(x)
			except IndexError:
				pass
		print invalidTreekeyList0
				
		treekeyListAux = []
		for x in self.treekeyList:
			if x not in invalidTreekeyList0:
				treekeyListAux.append(x)
		self.treekeyList = treekeyListAux
		print self.treekeyList
		
	def schemeListGen(self):
		print '+++++++++++++++schemeListGen++++++++++++++++++'
		self.schemeList = []	
		localTagSeq = [str(item[1]) for item in self.taggedSen]

		for i in range(len(self.treekeyList)):
			print '++++++++++++++++++doStageTTTT+++++++++++++++++'
			print self.ttcPrevious
			if i == 0:
				print self.treekeyList[i][0]+1
				aa = localTagSeq[:self.treekeyList[i][0]+1]
			else:
				print self.treekeyList[i-1][0]+1
				print self.treekeyList[i][0]+1
				aa = localTagSeq[self.treekeyList[i-1][0]+1:self.treekeyList[i][0]+1]
			print aa

			self.doStageTt(aa)
			print self.tagToCmpnt
		
		for i in range(len(self.treekeyList)):
			print '+++++++++++++++Starting the Loop++++++++++++++'
			#self.caseFlag0Gen(self.treekeyList, i)
			#print self.caseFlag0
		
			self.caseFlag1Gen(self.treekeyList, i)
	
			self.writeScheme0(self.auxListForCf1g)

			self.doStageCc(self.schemeTemp)
			self.writeScheme1(self.someVar)

		print self.schemeList
	
	def doStageTt(self, aa):
		#print '++++++++++++++++++doStageTt+++++++++++++++++++'
		queryPart0 = ''
		queryPart1 = ''
		memory0 = []
		adjust0 = 0
		indexStart = len(aa)
		indexEnd = len(aa)
		tagToCmpnt = []
		stepbwd = 0
		listExhaust = False
		while listExhaust == False:			
			sqlQueryCommon = "SELECT * FROM patterns_tt WHERE"
			queryPart1End = "=\'\' and patsuper NOT IN ('S','S_MOD','S_SBJ') ORDER BY freq DESC"
			if queryPart0 == '':
				queryPart0 = queryPart0 + " sub" + str(stepbwd) + "=\'/" + aa[-(stepbwd+adjust0+1)] + "\'"
				queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
			else:
				try:
					queryPart0 = queryPart0 + " and sub" + str(stepbwd) + "=\'/" + aa[-(stepbwd+adjust0+1)] + "\'"
					queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
				except IndexError:
					listExhaust = True

			sqlQuery0 = sqlQueryCommon + queryPart0
			sqlQuery1 = sqlQueryCommon + queryPart1
			#print sqlQuery0
			#print sqlQuery1
			
			self.db.query(sqlQuery0)
			result0 = self.db.store_result()
			numRows0 = result0.num_rows()
			self.db.query(sqlQuery1)
			result1 = self.db.store_result()
			numRows1 = result1.num_rows()
			
			# condition list exhastion
			if listExhaust == True:
				#tagToCmpnt.insert(0,[indexStart+adjustExt, indexEnd+adjustExt, memory0[0][0]])
				tagToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
				adjust0 = adjust0 + indexEnd - indexStart
				indexEnd = indexStart
				queryPart0 = ''
				queryPart1 = ''
				stepbwd = 0
				indexStart -= 1

			# condition for rollback
			elif numRows1 == 0:#numRows0 > 0 and 
				try:
					sqlQuery2 = sqlQuery0 + " and sub" + str(stepbwd+1) + "=\'/" + aa[-(stepbwd+adjust0+2)] + "\'"
					self.db.query(sqlQuery2)
					result2 = self.db.store_result()
					numRows2 = result2.num_rows()
				except IndexError:
					pass

				if numRows2 == 0:
					#tagToCmpnt.insert(0,[indexStart+adjustExt, indexEnd+adjustExt, memory0[0][0]])
					tagToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
					stepbwd = 0
				else:
					memory0 = []
					fetchedRow = result1.fetch_row()
					while fetchedRow:					
						memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
						fetchedRow = result1.fetch_row()				
					stepbwd += 1
					indexStart -= 1
			# condition for further search
			elif numRows0 > 0 and numRows1 > 0:
				memory0 = []
				fetchedRow = result1.fetch_row()
				while fetchedRow:					
					memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
					fetchedRow = result1.fetch_row()				
				stepbwd += 1
				indexStart -= 1
		
		for x in tagToCmpnt:
			x[0] += self.adjustExt
			x[1] += self.adjustExt

		self.tagToCmpnt = self.ttcPrevious + tagToCmpnt
		self.ttcPrevious = self.tagToCmpnt
		self.adjustExt += len(aa)

	# 모든 case마다 필요한 것은 아니므로 삭제 예정, 필요한 곳에서 재활용은 될듯
	"""
	def caseFlag0Gen(self, treekeyList, i):
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
	def caseFlag1Gen(self, treekeyList, i):
		#print '+++++++++++++++caseFlag1Gen+++++++++++++++++++'
		#print self.treekeyList
		#print self.tagToCmpnt
		onlyForCount = None
		for j in range(len(self.tagToCmpnt)):
			if self.treekeyList[i][0]+1 == self.tagToCmpnt[j][1]:
				self.auxListForCf1g = self.tagToCmpnt[:j+1]
				print self.auxListForCf1g
				break
		for j in range(len(self.tagToCmpnt)):
			try:
				if self.treekeyList[i+1][0]+1 == self.tagToCmpnt[j][1]:
					onlyForCount = self.tagToCmpnt[:j+1]
					print onlyForCount
					break
			except IndexError:
				onlyForCount = None

		"""
		onlyForCount = None
		for j in range(len(self.tagToCmpnt)):
			if self.treekeyList[i][0]+1 == self.tagToCmpnt[j][1]:
				self.auxListForCf1g = self.tagToCmpnt[:j+1]
				print self.auxListForCf1g
				break
		for j in range(len(self.tagToCmpnt)):
			try:
				if self.treekeyList[i+1][0]+1 == self.tagToCmpnt[j][1]:
					onlyForCount = self.tagToCmpnt[:j+1]
					print onlyForCount
					break
			except IndexError:
				onlyForCount = None

		flag10 = [item[2] for item in self.auxListForCf1g].count('NP_SBJ')
		if onlyForCount == None:
			flag11 = None
		else:
			flag11 = [item[2] for item in onlyForCount].count('NP_SBJ') - flag10

		self.caseFlag1 = [flag10, flag11]
		#print self.auxListForCf1g
		"""
	def writeScheme0(self, cddCmpntList):
		print '++++++++++++++++writeScheme0+++++++++++++++++++'
		#for y in self.taggedSen:
		#	print y[0] + ' ' + y[1] + '    ',
		#print '\n'
		#for y in self.ejlisedSen:
		#	print y[0] + ' ' + str(y[1]) + '   ',
		#print '\n'
		
		cpTypeToken = self.taggedSen[cddCmpntList[-1][1]-2:cddCmpntList[-1][1]]
		print cddCmpntList, " ", cpTypeToken
		for x in cpTypeToken:
			if str(x[1]) in ["ETM","ETN","EC","EF"]:
				cpType = str(x[1])
		#print cpType		

		print '_____Below is the place for your logs_____________\n\n'
		# Case: cpType == 'ETN'
		# 명사절
		if cpType == 'ETN':
			from tgCase1 import tgCase1
			cpTypeCaseN = tgCase1(self.ejlisedSen, self.taggedSen, self.db, cddCmpntList, cpTypeToken)

		# Case: cpType == 'ETM'
		# 관형절
		elif cpType == 'ETM':
			from tgCase2 import tgCase2
			cpTypeCaseN = tgCase2(self.ejlisedSen, self.taggedSen, self.db, cddCmpntList, cpTypeToken)
		# Case: cpType in ["EC,"EF"]
		# 부사절, 서술절, 인용절
		else:
			from tgCase0 import tgCase0
			cpTypeCaseN = tgCase0(self.ejlisedSen, self.taggedSen, self.db, cddCmpntList, cpTypeToken)
		# IMPORTANT! 
		# schemeIndex0: int
		# schemeIndex1: int
		# cfmdCmpntList: list
		#			e.g. :[0, 1, 'AP'], [1, 5, 'NP_AJT'], [5, 7, 'VP_MOD']
		# schemeAnnex: dictionary
		#			e.g. :{"case":"case1", "gita":"dd", "adjusted0":True}
		schemeIndex0 = cpTypeCaseN.schemeIndex0
		schemeIndex1 = cpTypeCaseN.schemeIndex1
		cfmdCmpntList = cpTypeCaseN.cfmdCmpntList
		schemeAnnex = cpTypeCaseN.schemeAnnex
			
		print '\n\n_____Above is the place for your logs_____________'
		
		self.schemeTemp = [cfmdCmpntList, schemeIndex0, schemeIndex1]
		self.schemeAnnexList.append(schemeAnnex)

	# 일단은 쓰고있지만 의미자로 절 끊기가 확정되고, 상위절에서의 기능확정까지 가능하다면 전체가 필요없는 메소드
	def doStageCc(self, schemeTempCc):
		#print '+++++++++++++++++++doStageCc++++++++++++++++++'
		if len(schemeTempCc[0]) == 1:
			furtherCmpntble = False
			cmpntToCmpnt = schemeTempCc[0]
		else:
			furtherCmpntble = True
		#print schemeTempCc[0]
		bb = [str(item[2]) for item in schemeTempCc[0]]

		while furtherCmpntble:
			print bb
			# assistant variables
			queryPart0 = ''
			queryPart1 = ''
			memory0 = []
			adjust0 = 0
			indexStart = len(bb)
			indexEnd = len(bb)
			cmpntToCmpnt = []
			stepbwd = 0
			listExhaust = False
			while listExhaust == False:
				sqlQueryCommon = "SELECT * FROM patterns_cc WHERE"
				#queryPart1End = "=\'\' and patsuper NOT IN ('S','S_MOD','S_SBJ') ORDER BY freq DESC"
				if queryPart0 == '':
					queryPart0 = queryPart0 + " sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+adjust0+1)] + "\'"
					queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
					#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
				else:
					try:
						queryPart0 = queryPart0 + " and sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+adjust0+1)] + "\'"
						queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
						#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
					except IndexError:
						listExhaust = True

				sqlQuery0 = sqlQueryCommon + queryPart0
				sqlQuery1 = sqlQueryCommon + queryPart1
				#print sqlQuery0
				#print sqlQuery1
				
				self.db.query(sqlQuery0)
				result0 = self.db.store_result()
				numRows0 = result0.num_rows()
				#print numRows0
				self.db.query(sqlQuery1)
				result1 = self.db.store_result()
				numRows1 = result1.num_rows()
				#print numRows1
				
				# condition list exhastion (& rollback?)
				if listExhaust == True:# and numRows0 > 0
					#print '_______condition list exhaustion_______'
					if len(memory0) == 0:
						cmpntToCmpnt.insert(0,[indexStart, indexEnd, bb[-(stepbwd+adjust0)]])
					else:
						cmpntToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					#print cmpntToCmpnt
					#print indexStart, ' ', indexEnd, ' ', adjust0
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
					stepbwd = 0
					indexStart -= 1
					#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
					#print '__________________________________________'				
				elif numRows1 == 0:# and numRows0 > 0
					#print '_______condition for rollback_______'
					#print memory0
					if len(memory0) == 0:
						#print bb[-(stepbwd+adjust0+1)]
						indexStart -= 1
						if indexStart == 0:
							listExhaust = True
						cmpntToCmpnt.insert(0,[indexStart, indexEnd, bb[-(stepbwd+adjust0+1)]])
					else:
						cmpntToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					#cmpntToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					#print cmpntToCmpnt
					#print indexStart, ' ', indexEnd, ' ', adjust0
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
					memory0 = []
					stepbwd = 0
					#indexStart -= 1
					#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
					#print '__________________________________________'		
				# condition for further search
				elif numRows0 > 0 and numRows1 > 0:
					#print '_______condition for further search_______'
					memory0 = []
					fetchedRow = result1.fetch_row()
					while fetchedRow:					
						if fetchedRow[0][3] not in ['S','S_MOD', 'S_SBJ']:
							memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
						fetchedRow = result1.fetch_row()
					stepbwd += 1
					indexStart -= 1
					#print memory0
					#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
					#print '__________________________________________'
			#print '________cmpntToCmpnt______________________'
			#print cmpntToCmpnt
			if len(cmpntToCmpnt) == 1:
				furtherCmpntble = False
			else:
				bb = [str(item[2]) for item in cmpntToCmpnt]
				print bb
			
		for j in range(len(self.tagToCmpnt)):
			#print self.schemeTemp[1], ' ', self.schemeTemp[2]
			if self.schemeTemp[1] == self.tagToCmpnt[j][0]:
				i0 = j
			if self.schemeTemp[2] == self.tagToCmpnt[j][1]:
				i1 = j
		#???
		self.someVar = [self.schemeTemp[1], self.schemeTemp[2], cmpntToCmpnt[0][2]]
		self.tagToCmpnt[i0:i1+1] = [self.someVar]
		# 다음 시행에서 완성된 tagToCmpnt수정
		print self.tagToCmpnt

	def writeScheme1(self, someVar):
		print '++++++++++++++++writeScheme1++++++++++++++++++'
		self.schemeList.append(self.someVar)#.append(self.schemeAnnex))
		print self.schemeList
		print self.schemeAnnexList