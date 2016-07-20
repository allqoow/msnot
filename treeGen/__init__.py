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
			if self.taggedSen[i][1] in ['EC','SF','ETN','ETM']:
				self.treekeyList.append(i)
		print self.treekeyList
		"""
		#
		for x in self.taggedSen:
			print x[0]+' ',
		print '\n'
		#
		
		#self.ngramSeqGen(2)
		#tt = self.ngramSeq
		#for i in range(len(tt)):
		#	if tt[i][0] in verblikes and tt[i][1] in endinglikes:
		#		indexList.append(i+2)

		#realIndexList = []
		# "보조용언"
		#'VV', 'EC', 'VV', 'EP'는 두가지 경우가 있다.
		# THIS BLOCK IS DESIGNED SPECIFIC TO NGRAM=2
		#for x in zip(indexList,indexList[1:]+[999]):
		#	if (x[1] - x[0]) != 2:
		#		realIndexList.append(x[0]+1)
		realIndexList = indexList
		
		# matrix clause는 SF를 포함하도록 했으면 좋겠는데...
		self.treekeyList[-1] = len(self.taggedSen)
		print self.treekeyList
		"""
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
		
		#for x in self.treekeyList:
		#	aa = localTagSeq[:x+1]
		x = 21
		aa = localTagSeq[:x+1]
		print aa

		# Stage _tt
		# assistant variables
		queryPart0 = ''
		queryPart1 = ''
		memory0 = []
		#memory1 = ''
		adjust0 = 0
		indexStart = len(aa)
		indexEnd = len(aa)
		tagToCmpnt = []
		stepbwd = 0
		#searchNeedTt = True
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
				#	queryPart0 = queryPart0 + " and sub" + str(stepbwd) + "=\'\'"
				#	#queryPart0 = " sub0=\'INVALID\'"
				#	listExhaust = True

			sqlQuery0 = sqlQueryCommon + queryPart0
			sqlQuery1 = sqlQueryCommon + queryPart1
			print sqlQuery0
			print sqlQuery1
			
			self.db.query(sqlQuery0)
			result0 = self.db.store_result()
			numRows0 = result0.num_rows()
			print numRows0
			self.db.query(sqlQuery1)
			result1 = self.db.store_result()
			numRows1 = result1.num_rows()
			print numRows1

			
			# condition list exhastion (& rollback?)
			if listExhaust == True:# and numRows0 > 0
				print '_______condition list exhaustion_______'		
				tagToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
				print tagToCmpnt
				#print indexStart, ' ', indexEnd, ' ', adjust0
				adjust0 = adjust0 + indexEnd - indexStart
				indexEnd = indexStart
				queryPart0 = ''
				queryPart1 = ''
				stepbwd = 0
				indexStart -= 1
				#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
				print '__________________________________________'				

			# condition for rollback
			elif numRows1 == 0:#numRows0 > 0 and 
				sqlQuery2 = sqlQuery0 + " and sub" + str(stepbwd+1) + "=\'/" + aa[-(stepbwd+adjust0+2)] + "\'"
				print sqlQuery2
				self.db.query(sqlQuery2)
				result2 = self.db.store_result()
				numRows2 = result2.num_rows()
				print numRows2
				if numRows2 == 0:
					print '_______condition for rollback_______'
					tagToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					print tagToCmpnt
					#print indexStart, ' ', indexEnd, ' ', adjust0
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
					stepbwd = 0
					#indexStart -= 1
					#print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
					print '__________________________________________'
				else:
					print '_______condition for further search_______'
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
				print '_______condition for further search_______'
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
		#for y in tempList:
		
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
			#memory1 = ''
			adjust0 = 0
			indexStart = len(bb)
			indexEnd = len(bb)
			cmpntToCmpnt = []
			stepbwd = 0
			#searchNeedTt = True
			listExhaust = False
			while listExhaust == False:
				sqlQueryCommon = "SELECT * FROM patterns_cc WHERE"
				queryPart1End = "=\'\' and patsuper NOT IN ('S','S_MOD','S_SBJ') ORDER BY freq DESC"
				if queryPart0 == '':
					queryPart0 = queryPart0 + " sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+adjust0+1)] + "\'"
					#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
					queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
				else:
					try:
						queryPart0 = queryPart0 + " and sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+adjust0+1)] + "\'"
						#queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + "=\'\' ORDER BY freq DESC"
						queryPart1 = queryPart0 + " and sub" + str(stepbwd+1) + queryPart1End
					except IndexError:
						listExhaust = True

				sqlQuery0 = sqlQueryCommon + queryPart0
				sqlQuery1 = sqlQueryCommon + queryPart1
				print sqlQuery0
				print sqlQuery1
				
				self.db.query(sqlQuery0)
				result0 = self.db.store_result()
				numRows0 = result0.num_rows()
				print numRows0
				self.db.query(sqlQuery1)
				result1 = self.db.store_result()
				numRows1 = result1.num_rows()
				print numRows1

				
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
					"""
					# condition for rollback
					elif numRows1 == 0 and numRows0 > 0
						print '_______condition for rollback_______'
						cmpntToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
						print cmpntToCmpnt
						print indexStart, ' ', indexEnd, ' ', adjust0
						adjust0 = adjust0 + indexEnd - indexStart
						indexEnd = indexStart
						queryPart0 = ''
						queryPart1 = ''
						stepbwd = 0
						#indexStart -= 1
						print indexStart, ' ', indexEnd, ' ', adjust0, ' ', str(stepbwd+adjust0)
						print '__________________________________________'
					"""
				elif numRows1 == 0:# and numRows0 > 0
					#print '_______condition for rollback_______'
					cmpntToCmpnt.insert(0,[indexStart, indexEnd, memory0[0][0]])
					#print cmpntToCmpnt
					#print indexStart, ' ', indexEnd, ' ', adjust0
					adjust0 = adjust0 + indexEnd - indexStart
					indexEnd = indexStart
					queryPart0 = ''
					queryPart1 = ''
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
						#if fetchedRow[0][3] not in ['S','S_MOD', 'S_SBJ']:
						memory0.append([fetchedRow[0][3], fetchedRow[0][2]])
						fetchedRow = result1.fetch_row()

					stepbwd += 1
					indexStart -= 1
					#print memory0
					#print '__________________________________________'
			print '________cmpntToCmpnt______________________'
			print cmpntToCmpnt
			#countV = 0
			#for y in cmpntToCmpnt:
			#	if y in ["VP","VP_AJT","VP_CMP","VP_MOD","VNP","VNP_AJT","VNP_CMP","VNP_MOD"]:
			#		countV += 1
			#if countV == 1:
			furtherCmpntble = False
			tagToCmpnt = cmpntToCmpnt




		"""
		searchNeedCc = True
		searchNeedCc1 = True
		while searchNeedCc:
			sqlQuery = "SELECT * FROM patterns_cc WHERE"
			if queryPart == '':
				queryPart = queryPart + " sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+1)] + "\'"
			else:
				try:
					queryPart = queryPart + " and sub" + str(stepbwd) + "=\'" + bb[-(stepbwd+1)] + "\'"
				except IndexError:
					queryPart = queryPart + " and sub" + str(stepbwd) + "=\'\'"
					#queryPart = " sub0=\'INVALID\'"
					listExhaust = True
					searchNeedCc1 = False
				#	pass
			print searchNeedCc1
			sqlQuery = sqlQuery + queryPart
			print sqlQuery
			memory0.append(sqlQuery)
			self.db.query(sqlQuery)
			r = self.db.store_result()
			fetchedRow = r.fetch_row()
			print fetchedRow

			# break condition
			if len(fetchedRow) == 0 or listExhaust == True:# or len(aa) == 0:
				rollback = True
				stepbwd += 1
				while rollback:
					stepbwd -= 1
					sqlQuery = memory0.pop() + " and sub" + str(stepbwd + 1) + "=\'\'"
					print sqlQuery
					self.db.query(sqlQuery)
					r = self.db.store_result()
					fetchedRow = True
					while fetchedRow:
						fetchedRow = r.fetch_row()
						if len(fetchedRow) > 0 and fetchedRow[0][3] not in ['S','S_MOD']:
							memory1 = fetchedRow[0][3]
							print memory1
							rollback = False
							#searchNeedCc = False
					print stepbwd
					
					#if len(memory0) == 0:
						
				
				print "_________________________________"
				print indexStart, stepbwd, adjust0
				indexStart = x - stepbwd - adjust0
				print "________INDEXSTART_________________________"
				indexStart = indexStart-1
				print indexStart, indexEnd, memory1
				print bb
				cmpntToCmpnt.insert(0,[indexStart, indexEnd,memory1])
				bb[indexStart:indexEnd] = []					

				# resetting some assistant variables
				print bb
				print cmpntToCmpnt
				queryPart = ''
				adjust0 += stepbwd
				indexEnd = indexStart
				stepbwd = 0
				print "_________________________________"
				print queryPart
				
				if listExhaust == True:
					searchNeedCc = False

				#searchNeedTt = False				
			elif len(fetchedRow) > 0:
				memory1 = fetchedRow[0][3]
				stepbwd += 1
		"""

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
		# case 0 문장을 ec로 끊어도 ㅁ문제거 없는 경우
		#if self.tagSeq.count('VX') == 0:
		#from case
		##	self.case = 0
		#else:
		#	self.case = 10
			
		# case 1 문장을 ec로 끊어도 ㅁ문제가 있는 경우(e.g. vv ec vv ec이런 게 존재 한다ㅡ)
		# if vv ec vv ec in ngram ...4 :
		#	self.case = 1
		# else:
		#	self.case = 0
		# case 0
		# No superordinate level component is found prior to the subordinate clauses.
		#if 'JX' not in self.tagSeq:
		#	self.case = 0
		#else:
		#	self.case = 1
"""
import _mysql
host = "allqoow001.cmfmq9ntkqns.ap-northeast-1.rds.amazonaws.com"
user = "allqoow"
password = "dhshsaes"
self.dbname = "msnotproto"
self.db = _mysql.connect(host,user,password,dbname)

bbbb = [['\xeb\x82\x98\xeb\x8a\x94', [0, 2]], ['\xec\x96\xb4\xec\xa0\x9c', [2, 3]], ['\xeb\x84\x88\xea\xb0\x80', [3, 5]], ['\xec\x86\x8c\xea\xb0\x9c\xec\x8b\x9c\xec\xbc\x9c\xec\xa4\x80', [5, 10]], ['\xec\x8b\x9d\xeb\x8b\xb9\xec\x97\x90\xec\x84\x9c', [10, 12]], ['\xeb\xb0\xa5\xec\x9d\x84', [12, 14]], ['\xeb\xa8\xb9\xeb\x8b\xa4\xea\xb0\x80', [14, 16]], ['\xeb\xb0\x94\xeb\x8b\xa5\xec\x97\x90', [16, 18]], ['\xec\x93\xb0\xeb\x9f\xac\xec\xa1\x8c\xeb\x8b\xa4.', [18, 22]]]
aaaa = [(u'\ub098', u'NP'), (u'\ub294', u'JX'), (u'\uc5b4\uc81c', u'MAG'), (u'\ub108', u'NP'), (u'\uac00', u'JKS'), (u'\uc18c\uac1c', u'NNG'), (u'\uc2dc\ud0a4', u'XSV'), (u'\uc5b4', u'EC'), (u'\uc8fc', u'VX'), (u'\u3134', u'ETM'), (u'\uc2dd\ub2f9', u'NNG'), (u'\uc5d0\uc11c', u'JKB'), (u'\ubc25', u'NNG'), (u'\uc744', u'JKO'), (u'\uba39', u'VV'), (u'\ub2e4\uac00', u'EC'), (u'\ubc14\ub2e5', u'NNG'), (u'\uc5d0', u'JKB'), (u'\uc4f0\ub7ec\uc9c0', u'VV'), (u'\uc5c8', u'EP'), (u'\ub2e4', u'EF'), (u'.', u'SF')]
aTree = treeGen(bbbb,aaaa,db)
"""
