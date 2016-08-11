#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

#from konlpy.tag import Komoran
#Komoran = Komoran()
import re
import selenium

import _mysql, msnotconfig2
host = msnotconfig2.host
user = msnotconfig2.user
password = msnotconfig2.password
dbname = msnotconfig2.dbname
db2 = _mysql.connect(host,user,password,dbname)
db2.query("set names utf8")

class sfGen():
	def __init__(self, driver, db, taggedSen):
		#self.searchInput = searchInput
		#self.searchInputAnnex = searchInputAnnex
		self.driver = driver
		self.db = db
		self.taggedSen = taggedSen

		from konlpy.tag import Komoran
		self.Komoran = Komoran()

		#self.dictSearchCommon

	def createSearchInputYongeon(self, yongeonPart):
		# 논항구조 가져오기
		index0 = yongeonPart[0]
		index1 = yongeonPart[1]
		searchInput = ""
		for x in self.taggedSen[index0:index1]:
			if "V" in x[1]:
				searchInput = searchInput + x[0]
			elif "J" in x[1]:
				break
			else:
				pass				
		searchInput = searchInput + "다"
		
		searchInputAnnex = {}
		searchInputAnnex["pos"] = "yongeon"

		print searchInput
		print searchInputAnnex
		self.searchInput = searchInput
		self.searchInputAnnex = searchInputAnnex

	def createSearchInputCheeon(self, cheeonPart):
		index0 = cheeonPart[0]
		index1 = cheeonPart[1]
		searchInput = ""
		print index0
		print index1
		for x in self.taggedSen[index0:index1]:
			if re.search(r"J[A-Z]+", x[1]) != None:
				pass
			else:
				searchInput = str(x[0])

		searchInputAnnex = {}
		searchInputAnnex["pos"] = "cheeon"

		print searchInput
		print searchInputAnnex
		self.searchInput = searchInput
		self.searchInputAnnex = searchInputAnnex

	def getSemanticFeature(self):
		dbSearchResult = self.retrieveFromDb(self.searchInput, self.searchInputAnnex)

		fetched = dbSearchResult.fetch_row()
		# case where there exist search results
		if fetched:
			while fetched:
				print fetched[0][6]
				fetched = dbSearchResult.fetch_row()
		# case where no search result has been found
		else:
			self.dictSearchCommon(self.searchInput, self.searchInputAnnex)
			self.dictSearchCheeon(self.searchInput, self.searchInputAnnex)
			self.insertIntoDb(self.searchInputAnnex)

		# searchInput 		: str
		# searchInputAnnex  : dict
		# returns 			: _mysql.result object 
	def retrieveFromDb(self, searchInput, searchInputAnnex):
		searchInputAnnex["pos"]
		sqlQuery = ""
		sqlQuery = sqlQuery + "SELECT * FROM sf_" + searchInputAnnex["pos"]
		sqlQuery = sqlQuery + " WHERE wordname REGEXP \'" + searchInput + "\'"
		print sqlQuery
		db2.query(sqlQuery)
		result = db2.store_result()
		#self.db.query(sqlQuery)
		#result = self.db.store_result()
		return result


	def dictSearchCommon(self, searchInput, searchInputAnnex):
		self.searchInput = searchInput
		self.searchInputAnnex = searchInputAnnex
		# direct to homepage of Daum한국어사전
		# select 
		self.driver.get("http://dic.daum.net/index.do?dic=kor")
		searchBox = self.driver.find_element_by_class_name("tf_keyword")
		searchInput = unicode(self.searchInput)
		searchBox.send_keys(searchInput)
		self.driver.find_element_by_class_name("btn_search").click()

		if re.search(r"search\.do\?", self.driver.current_url) != None:
			try:
				self.driver.find_element_by_class_name("txt_cleansch").click()
			except selenium.common.exceptions.NoSuchElementException:
				pass

		elems = self.driver.find_elements_by_class_name("fold_open")
		for x in elems:
			# folding unfolded boxes
			try:
				x.find_element_by_class_name("btn_fold").click()
			except selenium.common.exceptions.NoSuchElementException:
				pass		

	def dictSearchCheeon(self, searchInput, searchInputAnnex):
		ret = ""		
		searchInput = self.searchInput
		elems = self.driver.find_elements_by_class_name("box_word")
		
		for x in elems:
			retCommon = ""
			# unfolding folded boxes
			try:
				x.find_element_by_class_name("btn_fold").click()
			except selenium.common.exceptions.NoSuchElementException:
				#break
				pass
				#print "패쓰!"

			try:
				curl = self.driver.current_url
				kkw = curl.split("wordid=")[1].split("&")[0]
				kku = x.get_attribute("data-supid")			
				retCommon = retCommon + kkw + "|" + kku + "|" + pos.text + "|"
			except:
				break

			try:
				pos = x.find_element_by_class_name("tit_ex")
				#if pos.text not in ["명사","인칭 대명사"]:
				#	#print "체언이 아니자나!"
				#	break
			except:
				break

			try:
				retCommon = retCommon + x.find_element_by_class_name("txt_subword").text + "|"
			except selenium.common.exceptions.NoSuchElementException:
				retCommon = retCommon + searchInput + "|"

			try:
				retCommon = retCommon + x.find_element_by_class_name("txt_hanja").text + "|"
			except selenium.common.exceptions.NoSuchElementException:
				retCommon = retCommon + searchInput + "|"

			#print retCommon
			descs = x.find_elements_by_class_name("desc_item")
			#retSpecific = ""
			sfCfmd = ""
			descRaw = ""

			if retCommon.split("|")[2] not in ["명사", "의존 명사", "인칭 대명사"]:
				print "체언이 아니자나!"		
			else:
				for y in descs:
					descRaw = descRaw + y.text + "/"
					for z in y.text.split(".")[:-1]:
						desc = z.strip()
						desc = str(desc)
						sfCdd = ""
										
						#elif re.search(r"말한다", desc) != None:
						#	sfCdd = desc.split(" ")[-2]
						#부르는 또는 이르는...일컫는 말... 앞에서는 
						if re.search(r"통틀어 이르는 말", desc) != None:
							if re.search(r".+을", desc.split(" ")[-4]) != None:
								sfCdd = desc.split(" ")[-4].rstrip("을")
							elif re.search(r".+를", desc.split(" ")[-4]) != None:
								sfCdd = desc.split(" ")[-4].rstrip("를")

						elif re.search(r"높여 이르는 말", desc) != None:
							if re.search(r".+을", desc.split(" ")[-4]) != None:
								sfCdd = desc.split(" ")[-4].rstrip("을")
							elif re.search(r".+를", desc.split(" ")[-4]) != None:
								sfCdd = desc.split(" ")[-4].rstrip("를")
						else:
							sfCdd = desc.split(" ")[-1]
						#print sfCdd

						if self.Komoran.pos(sfCdd)[-1][1] == "ETN":
							sfCfmd = sfCfmd + "행동;"
						else:
							sfCfmd = sfCfmd + sfCdd + ";" 
					sfCfmd = sfCfmd + "/"
				#print sfCfmd
				retSpecific = sfCfmd + "|" + descRaw 
			
				ret = ret + retCommon + retSpecific + "\n"

			retCommon = ""
		
		self.dbInput = ret
		print ret
		return ret

	def dictSearchYongeon(self, searchInput, searchInputAnnex):
		ret = ""		
		searchInput = self.searchInput
		elems = self.driver.find_elements_by_class_name("box_word")

		for x in elems:
			# initialising variable
			retCommon = ""

			# unfolding folded boxes
			try:
				x.find_element_by_class_name("btn_fold").click()
			except selenium.common.exceptions.NoSuchElementException:
				pass

			# collecting kkw and kku (if any, break otherwise)
			try:
				curl = self.driver.current_url
				kkw = curl.split("wordid=")[1].split("&")[0]
				kku = x.get_attribute("data-supid")		
				retCommon = retCommon + kkw + "|" + kku + "|"
			except:
				break


			try:
				retCommon = retCommon + x.find_element_by_class_name("txt_subword").text + "|"
			except selenium.common.exceptions.NoSuchElementException:
				retCommon = retCommon + searchInput + "|"
				pass

			# collecting hanja (if any)
			try:
				retCommon = retCommon + x.find_elements_by_class_name("txt_pronounce")[1].text + "|"
			except (selenium.common.exceptions.NoSuchElementException, IndexError):
				try:
					retCommon = retCommon + self.driver.find_elements_by_class_name("txt_pronounce")[0].text + "|"
				except selenium.common.exceptions.NoSuchElementException:
					retCommon = retCommon + "NoHanja|"
			#print retCommon


			# for each description
			retSpecific = ""
			descs = x.find_elements_by_class_name("desc_item")
			for y in descs:				
				try:
					pos = x.find_element_by_class_name("tit_ex")
					if pos.text not in ["자동사","타동사","형용사"]:
						break
					#retSpecific = retSpecific + pos.text + "|"
				except selenium.common.exceptions.NoSuchElementException:
					#print "패쓰!"
					break

				#print y.text
				desc = str(y.text)

				try:
					argStruct = str(desc.split(")")[0].split("(")[1])
					#print ret1				
				
					taggedDesc = self.Komoran.pos(argStruct)
					#print taggedDesc
					
					argStructPat = []
					for i in range(len(taggedDesc)):
						if taggedDesc[i][1] == "JKS":
							if "JKS0" in argStructPat:
								argStructPat.append("JKS1")
							else:
								argStructPat.append("JKS0")
						elif re.search(r"JK[A-Z]+", taggedDesc[i][1]) != None:
							argStructPat.append(str(taggedDesc[i][1]))
					#print argStructPat

					switch = argStructPat[0]
					switchIndex = 1
					argStructRefined = ""
					for i in range(len(taggedDesc)):
						if re.search(r"N[A-Z]+", taggedDesc[i][1]) != None:
							argStructRefined = argStructRefined + taggedDesc[i][0] + "/" + switch[2:] + " " 
						elif re.search(r"JK[A-Z]+", taggedDesc[i][1]) != None and switchIndex < len(argStructPat):
							switch = argStructPat[switchIndex]
							switchIndex += 1
					retSpecific = pos.text + "|" + argStructRefined + "|" + desc
					#print retSpecific
					#print "ongoing"
				except (UnicodeDecodeError, IndexError):
					pass
				ret = ret + retCommon + retSpecific + "\n"
				#elif searchWordtype == "N":
				#	ret = ret + str(desc) + ";"	
			retCommon = ""
		self.dbInput = ret
		print ret
		return ret

	def insertIntoDb(self, searchInputAnnex):
		#print self.dbInput
		for x in self.dbInput.split("\n")[:-1]:
			dbInput = x
			print dbInput

			kkw = dbInput.split("|")[0]
			kku = dbInput.split("|")[1]
			
			if searchInputAnnex["pos"] == "cheeon":
				pos = unicode(dbInput.split("|")[2])
				wordname = dbInput.split("|")[3]
				wordname_hanja = dbInput.split("|")[4]
				
			elif searchInputAnnex["pos"] == "yongeon":
				pos = dbInput.split("|")[4]
				wordname = dbInput.split("|")[2]
				wordname_hanja = dbInput.split("|")[3]
				
			sf = dbInput.split("|")[5]	
			raw_desc = dbInput.split("|")[6]

			sqlQueryBh = ""
			sqlQueryBh = sqlQueryBh + "SELECT * FROM sf_" + searchInputAnnex["pos"]
			sqlQueryBh = sqlQueryBh + " WHERE kkw=\'" + kkw + "\' and kku=\'" + kku + "\'"
			#print sqlQueryBh
			#self.db.query(sqlQueryBh)
			db2.query(sqlQueryBh)
			#result = self.db.store_result()
			result = db2.store_result()

			if len(result.fetch_row()) == 0:
				sqlQuery = "INSERT INTO sf_" + searchInputAnnex["pos"]
				sqlQuery = sqlQuery + " (kkw, kku, pos, wordname, wordname_hanja, sf, raw_desc)"
				sqlQuery = sqlQuery + " VALUES ("
				sqlQuery = sqlQuery + "\'" + kkw + "\'" + ","
				sqlQuery = sqlQuery + "\'" + kku + "\'" + ","
				sqlQuery = sqlQuery + "\'" + pos + "\'" + ","
				sqlQuery = sqlQuery + "\'" + wordname + "\'" + ","
				sqlQuery = sqlQuery + "\'" + wordname_hanja + "\'" + ","
				sqlQuery = sqlQuery + "\'" + sf + "\'" + ","
				sqlQuery = sqlQuery + "\'" + raw_desc + "\'" + ")"
				print sqlQuery
				#self.db.query(sqlQuery)
				db2.query(sqlQuery)
			else:
				print "already inserted"

