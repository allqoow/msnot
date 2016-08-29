#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project   : msnot

import _mysql
import msnotconfig2
host = msnotconfig2.host
user = msnotconfig2.user
password = msnotconfig2.password
dbname = msnotconfig2.dbname
db = _mysql.connect(host, user, password, dbname)
db.query("set names utf8")



#result = db.store_result
#print result

db.query("SELECT * FROM sf_cheeon WHERE id>35000")
result = db.store_result()

#"INSERT INTO sf_cheeon (kkw, kku, pos, wordname, wordname_hanja, sf, raw_desc) VALUES ('kkw000167610','kku000210034','명사','아이콘','아이콘','것;/초상;/','[전산] 컴퓨터에 주는 명령을 문자나 기호, 그림 따위로 화면에 표시한 것./[종교] 그리스 정교회에서 모시는, 예수, 성모, 성도, 순교자 등의 초상./')"
count = 0 
fetched = result.fetch_row()
while fetched:
	print fetched[0][4]
	print fetched[0][6]
	print fetched[0][7]
	print "________________________________________________________________"
	#aa = fetched[0][-3].rstrip("/\n")

	fetched = result.fetch_row()
	count += 1
print count