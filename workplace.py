#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

# importing required modules
import os, re, sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
from pyPdf import PdfFileWriter, PdfFileReader

#output = PdfFileWriter()
input1 = PdfFileReader(file("Implementation.pdf", "rb"))
print dir(input1)
print input1.getNumPages()
print dir(input1.getPage(0))
aa = input1.getPage(1).extractText()
print len(aa)
"""
#'본'
'''
#input2 = str('이 법에 적용되는 연구과제는 기관생명윤리위원회(IRB)의 심의를 받도록 의무화되었습니다.')
#input3 = str('연구사업통합지원시스템을 망가뜨리기 위한 2가지 방법을 설명하려고 합니다.')
#input1 = str('나는 어제 친구랑 너가 소개시켜준 식당에서 밥을 먹다가 바닥에 쓰러졌다.')

input5 = str('미래창조과학부는 과학기술정책과 정보통신기술(ICT)에 관한 사무를 관장하는 중앙행정기관을 말한다.')
input6 = str('국토교통부는 국토의 체계적인 개발과 보존, 교통물류체계 구축 등의 사무를 관장하는 중앙행정기관을 말한다.')
'''

import MySQLdb
import _mysql
host = "allqoow001.cmfmq9ntkqns.ap-northeast-1.rds.amazonaws.com"
user = "allqoow"
password = "dhshsaes"
dbname = "msnotproto"
db = _mysql.connect(host,user,password,dbname)

direc = ".\\student\\senPattern\\"
with open(direc + 'patternRefined0717.txt','r') as dic:
	readlined = True
	count = 0
	while readlined:
	#for k in range(50):
		readlined = dic.readline()
		aa = readlined.split('|')
		if len(aa) > 3:
			freq = aa[0]
			patsuper = aa[1]
			patsub = []
			#"_tt", "_tc", "_cc"
			case = "_others"

			indicesTag = []
			indicesCmpnt = []
			ff = aa[2:]
			for i in range(len(aa[2:])):
				if re.search(r'/[A-Z]+', ff[i]) != None:
					indicesTag.append(i)
					patsub.append(ff[i])
				elif re.search(r'[A-Z_]+', ff[i]) != None:
					indicesCmpnt.append(i)
					patsub.append(ff[i])

			if len(indicesCmpnt) == 0:
				case = "_tt"
			elif len(indicesTag) == 0:
				case = "_cc"
			elif max(indicesTag) < min(indicesCmpnt):
				case = "_tc"
			else:
				case = "_others"

			cmpntlen = len(patsub)

			#print readlined
			#print str(cmpntlen) + ';' + freq + ';' + patsub + ';' + patsuper
			sqlQuery = "INSERT INTO patterns" + case
			
			queryPart0 = " (cmpntlen, freq, patsuper"
			queryPart1 = " VALUES (\'" + str(cmpntlen) + "\'"
			queryPart1 = queryPart1 + ",\'" + str(freq) + "\'"
			queryPart1 = queryPart1 + ",\'" + str(patsuper) + "\'"
			
			for i in range(len(patsub)):
				queryPart0 = queryPart0 + ", " + "sub" + str(i)
				queryPart1 = queryPart1 + ", " + "\'" + patsub[-(i+1)] + "\'" 
			queryPart0 = queryPart0 + ")"
			queryPart1 = queryPart1 + ")"
			sqlQuery = sqlQuery + queryPart0 + queryPart1
			

			#sqlQuery = sqlQuery +  + patsub + "\'" + "," 
			#sqlQuery = sqlQuery + "\'" + patsuper + "\'" + ")"
			print str(count)# + "    " + sqlQuery
			db.query(sqlQuery)
			count += 1
"""
sqlQuery = "SELECT * FROM tagpattern_proto"
db.query(sqlQuery)
r = db.store_result()
maxlen = 0
fetched = True
while fetched: 
	fetched = r.fetch_row()
	if len(fetched) != 0 and fetched[0][1] > maxlen:
		maxlen = fetched[0][1]
		
print maxlen
"""


