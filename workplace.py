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

import nltk
from nltk.corpus import propbank
print 'asdfa'

