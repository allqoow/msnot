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
		self.ngramSeq = self.ngramSeqGen(1)
		#self.tagSeq

		#self.tagSeqGen()
		self.treekeyListGen()
		self.schemeListGen()

	# deprecated
	def tagSeqGen(self):
		self.tagSeq = []
		args = []
		for x in self.taggedSen:
			self.tagSeq.append(str(x[1]))
	
	# n: integer
	def ngramSeqGen(self, n):
		args = []
		for i in range(n):
			args.append(self.taggedSen[i:][1])
		self.ngramSeq = zip(*args)	

	def treekeyListGen(self):
		#verblikes = ['XSV', 'XSA', 'VV', 'VA', 'VX', 'VCP', 'VCN']
		#endinglikes = ['EP', 'EF', 'EC', 'ETN', 'ETM']
		self.treekeyList = []
		for i in range(len(self.taggedSen)):
			if self.taggedSen[i][1] in ['EC','SF']:#,'ETN','ETM']:
				self.treekeyList.append(i)
		print self.treekeyList


		#realIndexList = []
		# "보조용언"
		#'VV', 'EC', 'VV', 'EP'는 두가지 경우가 있다.
		# THIS BLOCK IS DESIGNED SPECIFIC TO NGRAM=2
		#for x in zip(indexList,indexList[1:]+[999]):
		#	if (x[1] - x[0]) != 2:
		#		realIndexList.append(x[0]+1)
		#realIndexList = indexList
		
		# matrix clause는 SF를 포함하도록 했으면 좋겠는데...
		self.treekeyList[-1] = len(self.taggedSen)
		print self.treekeyList
		
	def schemeListGen(self):
		# 띄어쓰기지점이 아닌 곳의 treekey는 모두 제거
		# case-independent treekey filtering and updating treekeyList accordingly
		invalidTreekeyList0 = []
		for x in self.ejlisedSen:
			invalidTreekeyList0 = invalidTreekeyList0 + range(x[1][0], x[1][1]-1)
		print invalidTreekeyList0
				
		treekeyListAux = []
		for x in self.treekeyList:
			if x not in invalidTreekeyList0:
				treekeyListAux.append(x)
		self.treekeyList = treekeyListAux
		print self.treekeyList

		# case판단
		# determine the case
		#self.determineCase()
		
		# schemeList작성
		# establish schemeList
		self.schemeList = []	

		localTagSeq = [str(item[1]) for item in self.taggedSen]
		ctcPrevious = []
		adjustExt = 0
		for i in range(len(self.treekeyList)):
			if i == 0:
				aa = localTagSeq[:self.treekeyList[i]+1]
			else:
				aa = localTagSeq[self.treekeyList[i-1]+1:self.treekeyList[i]+1]
			print aa

			# Stage _tt
			# assistant variables
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
					#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
					queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
				else:
					try:
						queryPart0 = queryPart0 + " and sub" + str(stepbwd) + "=\'/" + aa[-(stepbwd+adjust0+1)] + "\'"
						#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
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
				#print numRows0
				self.db.query(sqlQuery1)
				result1 = self.db.store_result()
				numRows1 = result1.num_rows()
				#print numRows1
				
				# condition list exhastion (& rollback?)
				if listExhaust == True:# and numRows0 > 0
					#print '_______condition list exhaustion_______'		
					tagToCmpnt.insert(0,[indexStart+adjustExt, indexEnd+adjustExt, memory0[0][0]])
					#print tagToCmpnt
					#print indexStart, ' ', indexEnd, ' ', adjust0
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
					stepbwd = 0
					indexStart -= 1
					#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
					#print '__________________________________________'				

				# condition for rollback
				elif numRows1 == 0:#numRows0 > 0 and 
					sqlQuery2 = sqlQuery0 + " and sub" + str(stepbwd+1) + "=\'/" + aa[-(stepbwd+adjust0+2)] + "\'"
					#print sqlQuery2
					self.db.query(sqlQuery2)
					result2 = self.db.store_result()
					numRows2 = result2.num_rows()
					#print numRows2
					if numRows2 == 0:
						#print '_______condition for rollback_______'
						tagToCmpnt.insert(0,[indexStart+adjustExt, indexEnd+adjustExt, memory0[0][0]])
						#print tagToCmpnt
						#print indexStart, ' ', indexEnd, ' ', adjust0
						adjust0 = adjust0 + indexEnd - indexStart
						indexEnd = indexStart
						queryPart0 = ''
						queryPart1 = ''
						stepbwd = 0
						#indexStart -= 1
						#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
						#print '__________________________________________'
					else:
						#print '_______condition for further search_______'
						memory0 = []
						fetchedRow = result1.fetch_row()
						while fetchedRow:					
							#print fetchedRow
							memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
							fetchedRow = result1.fetch_row()				
						
						stepbwd += 1
						indexStart -= 1
						#print memory0
						#print '__________________________________________'	

				# condition for further search
				elif numRows0 > 0 and numRows1 > 0:
					#print '_______condition for further search_______'
					memory0 = []
					fetchedRow = result1.fetch_row()
					while fetchedRow:					
						#print fetchedRow
						memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
						fetchedRow = result1.fetch_row()				
					
					stepbwd += 1
					indexStart -= 1
					#print memory0
					#print '__________________________________________'		
				
			print '__________tagToCmpnt______________________'
			print tagToCmpnt
			tempList = tagToCmpnt

			tagToCmpnt = ctcPrevious + tagToCmpnt
			print '__________tagToCmpnt_amended______________'
			print tagToCmpnt

			# Stage _cc
			furtherCmpntble = True
			while furtherCmpntble:
				print '+++++++++++++++++++++++++++++++++++++++++'
				print '+++++++++++++++++++++++++++++++++++++++++'
				print tagToCmpnt
				bb = [str(item[2]) for item in tagToCmpnt]
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
						if len(memory0) == 0:
							cmpntToCmpnt.insert(0,[indexStart, indexEnd, bb[-(stepbwd+adjust0)]])
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
						#print '__________________________________________'
				print '________cmpntToCmpnt______________________'
				print cmpntToCmpnt
				
				furtherCmpntble = False
				#tagToCmpnt = cmpntToCmpnt
				forRearrangement0 = cmpntToCmpnt


			# do final ordering
			ctcPrevious = forRearrangement0
			finalBreak = forRearrangement0
			fr1 = finalBreak[-1]
			print fr1
			indexToCtc0 = fr1[0]
			indexToCtc1 = fr1[1]
			print tagToCmpnt

			schemeIndex0 = tagToCmpnt[indexToCtc0][0]
			schemeIndex1 = tagToCmpnt[indexToCtc1-1][1]
			schemeCmpntSuper = fr1[2]
			print schemeIndex0 
			print schemeIndex1
			print schemeCmpntSuper
			#localTagSeq = [str(item[1]) for item in self.taggedSen]
			#print localTagSeq[schemeIndex0:schemeIndex1]
			self.schemeList.append([schemeIndex0, schemeIndex1, schemeCmpntSuper])
			adjustExt += len(aa)
	

		# Stage 5-1: 대등절 나누기,
		# Case 0
		# the simplest case...  
		#EC앞에 조사가 등장하지 않는다.
		# No superordinate level component is found prior to the subordinate clauses.
		"""
		if self.case == 0:
			adjust = 0
			for i in self.treekeyList:
				#localTagSeq = self.tagSeq
				localTagSeq = self.taggedSen
				mainPointer = i-adjust
				print localTagSeq
				print mainPointer

				while True:
					# breakout from the loop if some conditions are satified
					# OR when mainPointer reaches the beginning of the list
					if mainPointer == 0:
						if localTagSeq[i-adjust] == 'ETM':
							#self.schemeList.append([mainPointer, i-adjust, 'MM'])
							self.schemeList.append([mainPointer, i+1, 'MM'])
							localTagSeq[mainPointer:i-adjust] = [('uhuhu','MM')]
						elif localTagSeq[i-adjust][1] == 'EC':
							#self.schemeList.append([mainPointer, i-adjust, 'MAG'])
							self.schemeList.append([mainPointer, i+1, 'MAG'])
							localTagSeq[mainPointer:i-adjust] = [('uhuhu','MAG')]
						#elif localTagSeq[i-adjust] == 'EP':
						#	self.schemeList.append([mainPointer, i-adjust, 'MAG'])
						#	localTagSeq[mainPointer:i-adjust+1] = ['MAG']
						elif localTagSeq[i-adjust+1][1] == 'SF':
							#self.schemeList.append([mainPointer, i-adjust, 'MatrixClause'])
							self.schemeList.append([mainPointer, i+1, 'MatrixClause'])
						adjust = i-mainPointer
						break			
					else:
						mainPointer -= 1
		"""
		# Case 1
		# 주어가 있다

		print self.schemeList
		print '\n'
		# just for inspiration, no practical use for now
		#subPointer0 = 0
		#subPointer1 = 0
		#memory0 = 0
		#caseSpecificTagSet = ['JX']	
		#localTagSeq[mainPointer-1][1] in caseSpecificTagSet or

	def determineCase(self):
		pass


