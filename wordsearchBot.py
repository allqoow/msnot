#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot
#
# Step 3
#
# in order not to import the same modules redundantly
def atTermsNaver(searchWord, driver, re):
	targetURL = "http://terms.naver.com/search.nhn?query=" + searchWord + "&searchType=&dicType=&subject="
	driver.get(targetURL)
	searchResults = driver.find_elements_by_tag_name("a")

	cddList = []
	for x in searchResults:
		targetText = str(x.text)
		if re.search(searchWord+r' +', targetText, re.UNICODE):
			cdd = ""
			for c in x.text:
				if ord(c) in range(32,127):
					cdd += c
			if re.search(r'[a-zA-Z]',cdd):
				#print cdd
				cdd = str(cdd)
				cdd = re.sub(r'\[\W*',r'',cdd)
				cdd = re.sub(r'\W*\]',r'',cdd)
				cdd = cdd.strip()
				cddList.append(cdd)

	# do coherency test, then...
	if len(cddList) == 0:
		cddList.append('No official translation')

	return cddList[0]

	# or send query to other scripts?
	#if len(cddList) == 0:
	#	print "EMPTY"

# driver.get("https://translate.google.co.kr/")
# searching from http://elaw.klri.re.kr/kor_service/main.do
# http://elaw.klri.re.kr/kor_service/lawView.do?hseq=1&lang=ENG