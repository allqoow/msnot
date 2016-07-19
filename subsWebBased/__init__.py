#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

# 3-1. searchBot/Bot selector
# 3-2. compound noun constructor
class subsWebBased():
	def __init__(self, driver):
		pass

'''
aliasMapping = []
aliasCommon = 'mnProper'
aliasId = 0
for x in cc[1].split(' '):
	# 검색대상을 선정하는 기준은?(1)
	# NNG가 한 어절에서 세번 나오면 검색대상이 되어야 할까? 연접빈도를 통해서 예측되지 않는 단어라면 검색대상?
	# 띄어쓰기를 전부 붙이고 다시 재구성?
	if len(re.findall('NNG', x)) >= 3:
		#print x
		xDecomposed = re.sub(r'__[0-9]+', '', x).split('+')
		searchWord = ''
		xBacks = ''
		for i in range(len(xDecomposed)):
			#이/VCP+다/EF+./SF
			if re.search(r'/J[A-Z]+|이/VCP|다/EF|\./SF', xDecomposed[i]) != None:
				xBacks += xDecomposed[i]
			elif re.search(r'/S[A-Z]+', xDecomposed[i]) != None:
				pass
			else:
				searchWord += xDecomposed[i].split('/')[0]
		
		# strip! strip!
		searchWord = str(searchWord.strip())
		# 자체 라이브러리?
		# 어떤 서치봇을 돌릴까?(2)
		from wordsearchBot import atTermsNaver
		#print 'searching the word form Naver...'
		aa = atTermsNaver(searchWord, driver, re)
		aliasMapping.append([aliasCommon + str(aliasId), aa])
		x = aliasCommon + str(aliasId) + '/SL+' + xBacks + str(aliasMapping[aliasId])#NNG?
		aliasId += 1
		
	print x
print aliasMapping
'''
# 법령정보사이트
# KISS