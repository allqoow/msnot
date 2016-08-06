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

#userInput = str('나는 너를 때리고 철수는 영희를 찼고 명수는 걔를 죽였다.')
#userInput = str('사람이 하늘에서 떨어지면 대부분 죽는다.')
userInput = str('드디어 연극계에도 예쁜 일이 오고 있다.')
#userInput = str('내가 소개해 준 식당에서 먹어라.')
input5 = str('미래창조과학부는 과학기술정책과 정보통신기술(ICT)에 관한 사무를 관장하는 중앙행정기관을 말한다.')
input6 = str('국토교통부는 국토의 체계적인 개발과 보존, 교통물류체계 구축 등의 사무를 관장하는 중앙행정기관을 말한다.')
'''

#import nltk
#from nltk.corpus import propbank
import _mysql, msnotconfig
host = msnotconfig.host
user = msnotconfig.user
password = msnotconfig.password
dbname = msnotconfig.dbname
db = _mysql.connect(host,user,password,dbname)

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#driver = webdriver.PhantomJS()
driver = webdriver.Firefox()

#searchInput = unicode("철수")
#searchWordtype = "N"
def dictSearchByWord(searchInput, searchWordtype, driver):
	searchInput = unicode(searchInput)
	driver.get("http://dic.daum.net/index.do?dic=kor")
	searchBox = driver.find_element_by_class_name("tf_keyword")
	searchBox.send_keys(searchInput)
	driver.find_element_by_class_name("btn_search").click()

	if re.search(r"search\.do\?", driver.current_url) != None:
		driver.find_element_by_class_name("txt_cleansch").click()

	elems = driver.find_elements_by_class_name("fold_open")
	for x in elems:
		try:
			x.find_element_by_class_name("btn_fold").click()
		except selenium.common.exceptions.NoSuchElementException:
			pass

	elems = driver.find_elements_by_class_name("box_word")

	bb = ""
	for x in elems:
		try:
			x.find_element_by_class_name("btn_fold").click()
		except selenium.common.exceptions.NoSuchElementException:
			print "패쓰!"

		try:
			bb = bb + x.find_element_by_class_name("txt_subword").text + ";"
		except selenium.common.exceptions.NoSuchElementException:
			print "패쓰!"
			bb = bb + searchInput + ";"
		
		curl = driver.current_url

		pos = x.find_element_by_class_name("tit_ex")
		print type(pos.text)
		print len(pos.text)
		descs = x.find_elements_by_class_name("desc_item")
		for y in descs:			
			print y.text
			desc = str(y.text)
			if searchWordtype == "V":
				argStruct = desc.split(")")[0][1:]
				#print argStruct
				bb = bb + str(argStruct) + ";"
			elif searchWordtype == "N":
				bb = bb + str(desc) + ";"	
		bb = bb + "|"
	return bb

bb = dictSearchByWord("웃다", "V", driver)
print bb
from konlpy.tag import Komoran
Komoran = Komoran()

for x in bb.split("|")[:-1]:
	print "+++++++++++++++++++++++++"
	wordName = x.split(";")[0]
	wordMeaning = x.split(";")[1]

	# consider only the very first description
	cc = wordMeaning.split(".")[0]
	ejs = cc.split(" ")
	print cc
	print type(cc)
	# "통틀어 이르는 말"
	#if re.search(r"통틀어 이르는 말", cc) != None:
	if "통틀어 이르는 말" in cc:
		ejIndex = -4
	else:
		ejIndex = -1

	# test ETM
	etmTester = Komoran.pos(ejs[ejIndex])
	print etmTester
	if str(etmTester[-1][1]) == "ETM":
		nextSearchInput = str(etmTester[0][0]) + str("다")
	else:
		nextSearchInput = str(etmTester[0][0])
	
	#for y in b:
	#	print y[0]," ",y[1], "  ;", 
	#print "\n"

	print nextSearchInput
	"""
	b = Komoran.pos(wordMeaning)
	for y in b:
		print y[0]," ",y[1], "  ;", 
	print "\n"
	"""


driver.close()
#driver.quit()
