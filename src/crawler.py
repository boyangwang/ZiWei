# -*- coding: utf-8 -*-
import sys
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
import codecs
_open_func_bak = open # Make a back up, just in case
open = codecs.open

import time
from dbDrive import DBDriver
from multiprocessing import Pool
import json
import urllib
import urllib2
import socket
from bs4 import BeautifulSoup as BS
from models.BenMingPan import BenMingPan
from models.DaXianPan import DaXianPan 
from models.LiuNianPan import LiuNianPan
from models.Pan import Pan
from datetime import date
from dateutil.rrule import rrule, DAILY

def crawlResponseWithInputs(inputs):
	url = 'http://www.zhycw.com/pp/zw.aspx'
	form_data = inputs
	form_data['submit'] = '%E5%BC%80%E5%A7%8B%E6%8E%92%E7%9B%98',
	form_data_encoded = urllib.urlencode(form_data)
	req = urllib2.Request(url, form_data_encoded)
	res = urllib2.urlopen(req)
	res = res.read()
	return res

# 0 10 11 9
# 1       8
# 2       7
# 3 4  5  6
def createPanObjectFromInputs(inputs, http=True):
	try:
		name = Pan.getName(inputs)
		print 'START: ', name
		driver = DBDriver()
		
		results = driver.collection.find({
			'name': name
		})

		# print 'LEN: ', results.limit(1).count()

		if (results.limit(1).count() >= 1):
			print 'EXIST: ', name
			return

		if (http):	
			page = crawlResponseWithInputs(inputs)
		else:
			page = open('sample-response.html', 'r').read()

		if (inputs['mode'] == 1):
			panObj = BenMingPan(inputs, page)
		elif (inputs['mode'] == 2):
			panObj = DaXianPan(inputs, page)
		elif (inputs['mode'] == 3):
			panObj = LiuNianPan(inputs, page)
		else:
			# unrecognized mode
			panObj = None

		panObj.initData()
		jsonObj = panObj.serialize()
		driver.insert(jsonObj)
		print 'DONE: ', name
		# print panObj.serializeToFile()

		return panObj
	except Exception as e:
		print 'ERROR: ', Pan.getName(inputs)
		print str(sys.exc_info()[0]) + '\n' + str(e.__doc__) + '\n' + str(e.message)
		errlog = open('data/errlog-' + Pan.getName(inputs), 'w')
		errlog.write(str(sys.exc_info()[0]) + '\n' + str(e.__doc__) + '\n' + str(e.message))
		# traceback.print_tb(sys.exc_info()[3], None, errlog)
		traceback.print_exc(None, errlog)

		return None

def createStarList():
	starList = list()
	baseUrl = 'http://www.zhycw.com/pp/showstar.aspx?id='
	done = False
	for i in range(1, 101):
		if (i == 31):
			starList.append(u'天厨')
			continue

		if (done):
			print 'skip: ' + str(i)
			done = False
			continue
		print i
		url = baseUrl + str(i)
		req = urllib2.Request(url)
		res = urllib2.urlopen(req)
		bs = BS(res.read())
		
		if (bs.find('h1') != None): # .string.find(u'本页面暂时出错，正在检查！') != -1):
			print 'error: ', i
			starList.append(str(i))
			continue 
		
		firstAttempt = (bs.find_all('div')[2].contents[1].string.strip())
		puncIndex = firstAttempt.find(u'、')
		if (puncIndex == -1):
			print 'first'
			print firstAttempt[:2]
			starList.append(firstAttempt[:2])
		else:
			print 'second'
			firstInPair = firstAttempt[:puncIndex]
			secondInPair = firstAttempt[puncIndex+1:puncIndex+3]
			done = True
			print firstInPair
			print secondInPair
			starList.append(firstInPair)
			starList.append(secondInPair)

	
	starListFile = open('starList.json', 'w', encoding="utf-8")
	starListString = json.dumps(starList, ensure_ascii=False)
	print starListString
	starListFile.write(starListString.encode('utf-8'))
	return starList

def readStarList():
	starListFile = open('starList.json', 'r', encoding="utf-8")
	starList = json.load(starListFile)
	return starList

def createInputsArray(a, b):
	for dt in rrule(DAILY, dtstart=a, until=b):
		templateInput = {
			'y':int(dt.strftime('%Y')),
			'm':int(dt.strftime('%m')),
			'd':int(dt.strftime('%d')),
			'h':0,
			'min':0,
			'sex':0,
			'mode':1,
		}
		for h in range(0,24,2):
			for sex in range(0,2):
				for mode in range(1,4):
					currentInput = templateInput.copy()
					currentInput['h'] = h
					currentInput['sex'] = sex
					currentInput['mode'] = mode
					yield currentInput	

def main():
	
	inputs = {
		'y':1990,
		'm':1,
		'd':1,
		'h':0,
		'min':0,
		'sex':1,
		'mode':1,
	}
	
	# starList = readStarList() #createStarList() 



	p = Pool(3)

	time.clock()
	
	inputsArray = [input for input in createInputsArray(date(1990, 1, 1), date(2000, 1, 1))]
	print 'GENERATOR DONE'
	result = p.map(createPanObjectFromInputs, inputsArray)

	# for inputs in inputsArray:
	# 	createPanObjectFromInputs(inputs)

	# panObj = createPanObjectFromInputs(inputs, http=True)

	print 'Elapsed time: ' + str(time.clock())

	# for y in range(1990, 1992):
	# 	for m in range(1, 3):
	# 		for d in range(1, 3):
	# 			for h in range(0, 24, 2):
	# 				for sex in range(0, 2):
	# 					for mode in range(1, 4):
	# 						inputs['y'] = y
	# 						inputs['m'] = m
	# 						inputs['d'] = d
	# 						inputs['h'] = h
	# 						inputs['sex'] = sex
	# 						inputs['mode'] = mode
	# 						panObj = createPanObjectFromInputs(inputs, http=True)
	# 						name = panObj.serialize()

	

	# correct = open('1-0-0-1-1-1-1990-out.json', 'r', encoding="utf-8").read()
	# current = open(name, 'r', encoding="utf-8").read()

	# for i in range(min(len(correct), len(current))):
	# 	if (correct[i] != current[i]):
	# 		print 'ERROR: ', i
	# 		break;

if __name__ == '__main__':
	main()