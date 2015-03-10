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
def createPanObjectFromInputs(inputs, http=True, offline=False):
	try:
		name = Pan.getName(inputs)
		print 'START: ', name
		
		if (not offline): 
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
		if (not offline):
			driver.insert(jsonObj)
		else:
			panObj.serializeToFile()
		print 'DONE: ', name
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

def buildStarExplanation():
	obj = {
		"紫微": {'zhu': 1, 'explanation': {}},
		"天机": {'zhu': 1, 'explanation': {}},
		"太阳": {'zhu': 1, 'explanation': {}},
		"武曲": {'zhu': 1, 'explanation': {}},
		"天同": {'zhu': 1, 'explanation': {}},
		"廉贞": {'zhu': 1, 'explanation': {}},
		"天府": {'zhu': 1, 'explanation': {}},
		"太阴": {'zhu': 1, 'explanation': {}},
		"贪狼": {'zhu': 1, 'explanation': {}},
		"巨门": {'zhu': 1, 'explanation': {}},
		"天相": {'zhu': 1, 'explanation': {}},
		"天梁": {'zhu': 1, 'explanation': {}},
		"七杀": {'zhu': 1, 'explanation': {}},
		"破军": {'zhu': 1, 'explanation': {}},
		"文昌": {'zhu': 0, 'explanation': ''},
		"文曲": {'zhu': 0, 'explanation': ''},
		"左辅": {'zhu': 0, 'explanation': ''},
		"右弼": {'zhu': 0, 'explanation': ''},
		"天魁": {'zhu': 0, 'explanation': ''},
		"天钺": {'zhu': 0, 'explanation': ''},
		"擎羊": {'zhu': 0, 'explanation': ''},
		"陀罗": {'zhu': 0, 'explanation': ''},
		"火星": {'zhu': 0, 'explanation': ''},
		"铃星": {'zhu': 0, 'explanation': ''},
		"地空": {'zhu': 0, 'explanation': ''},
		"地劫": {'zhu': 0, 'explanation': ''},
		"禄存": {'zhu': 0, 'explanation': ''},
		"天马": {'zhu': 0, 'explanation': ''},
		"天官": {'zhu': 0, 'explanation': ''},
		"天福": {'zhu': 0, 'explanation': ''},
		"天厨": {'zhu': 0, 'explanation': ''},
		"天刑": {'zhu': 0, 'explanation': ''},
		"天姚": {'zhu': 0, 'explanation': ''},
		"解神": {'zhu': 0, 'explanation': ''},
		"天巫": {'zhu': 0, 'explanation': ''},
		"天月": {'zhu': 0, 'explanation': ''},
		"阴煞": {'zhu': 0, 'explanation': ''},
		"台辅": {'zhu': 0, 'explanation': ''},
		"封诰": {'zhu': 0, 'explanation': ''},
		"天空": {'zhu': 0, 'explanation': ''},
		"天哭": {'zhu': 0, 'explanation': ''},
		"天虚": {'zhu': 0, 'explanation': ''},
		"龙池": {'zhu': 0, 'explanation': ''},
		"凤阁": {'zhu': 0, 'explanation': ''},
		"红鸾": {'zhu': 0, 'explanation': ''},
		"天喜": {'zhu': 0, 'explanation': ''},
		"孤辰": {'zhu': 0, 'explanation': ''},
		"寡宿": {'zhu': 0, 'explanation': ''},
		"蜚廉": {'zhu': 0, 'explanation': ''},
		"破碎": {'zhu': 0, 'explanation': ''},
		"51": {'zhu': 0, 'explanation': ''},
		"52": {'zhu': 0, 'explanation': ''},
		"天德": {'zhu': 0, 'explanation': ''},
		"月德": {'zhu': 0, 'explanation': ''},
		"天才": {'zhu': 0, 'explanation': ''},
		"天寿": {'zhu': 0, 'explanation': ''},
		"三台": {'zhu': 0, 'explanation': ''},
		"八座": {'zhu': 0, 'explanation': ''},
		"恩光": {'zhu': 0, 'explanation': ''},
		"天贵": {'zhu': 0, 'explanation': ''},
		"截空": {'zhu': 0, 'explanation': ''},
		"旬空": {'zhu': 0, 'explanation': ''},
		"天使": {'zhu': 0, 'explanation': ''},
		"天伤": {'zhu': 0, 'explanation': ''},
		"博士": {'zhu': 0, 'explanation': ''},
		"力士": {'zhu': 0, 'explanation': ''},
		"青龙": {'zhu': 0, 'explanation': ''},
		"小耗": {'zhu': 0, 'explanation': ''},
		"将军": {'zhu': 0, 'explanation': ''},
		"奏书": {'zhu': 0, 'explanation': ''},
		"飞廉": {'zhu': 0, 'explanation': ''},
		"喜神": {'zhu': 0, 'explanation': ''},
		"病符": {'zhu': 0, 'explanation': ''},
		"大耗": {'zhu': 0, 'explanation': ''},
		"伏兵": {'zhu': 0, 'explanation': ''},
		"官府": {'zhu': 0, 'explanation': ''},
		"将星": {'zhu': 0, 'explanation': ''},
		"攀鞍": {'zhu': 0, 'explanation': ''},
		"岁驿": {'zhu': 0, 'explanation': ''},
		"息神": {'zhu': 0, 'explanation': ''},
		"华盖": {'zhu': 0, 'explanation': ''},
		"劫煞": {'zhu': 0, 'explanation': ''},
		"灾煞": {'zhu': 0, 'explanation': ''},
		"天煞": {'zhu': 0, 'explanation': ''},
		"指背": {'zhu': 0, 'explanation': ''},
		"咸池": {'zhu': 0, 'explanation': ''},
		"月煞": {'zhu': 0, 'explanation': ''},
		"亡神": {'zhu': 0, 'explanation': ''},
		"岁建": {'zhu': 0, 'explanation': ''},
		"晦气": {'zhu': 0, 'explanation': ''},
		"丧门": {'zhu': 0, 'explanation': ''},
		"贯索": {'zhu': 0, 'explanation': ''},
		"官符": {'zhu': 0, 'explanation': ''},
		"小耗": {'zhu': 0, 'explanation': ''},
		"大耗": {'zhu': 0, 'explanation': ''},
		"龙德": {'zhu': 0, 'explanation': ''},
		"白虎": {'zhu': 0, 'explanation': ''},
		"天德": {'zhu': 0, 'explanation': ''},
		"吊客": {'zhu': 0, 'explanation': ''},
		"病符": {'zhu': 0, 'explanation': ''},
	}
	for key,value in obj.iteritems():
		if (obj[key]['zhu'] == 0):
			obj[key]['explanation'] = key + u'星注释：暂无'
		else:
			for gong in [u'身命宫', u'父母宫', u'福德宫', u'田宅宫', u'官禄宫', u'仆役宫', u'迁移宫', u'疾厄宫', u'财帛宫', u'子女宫', u'夫妻宫', u'兄弟宫']:
				exp = key + u'星在' + gong + u'注释：暂无'
				obj[key]['explanation'][gong] = exp
	starExplanation = open('starExplanation.json', 'w')
	json.dump(obj, starExplanation, ensure_ascii=False, indent=2);

def main():
	buildStarExplanation()
	inputs = {
		'y':1990,
		'm':1,
		'd':1,
		'h':0,
		'min':0,
		'sex':1,
		'mode':1,
	}

	# p = Pool(6)

	time.clock()
	
	inputsArray = [input for input in createInputsArray(date(1990, 1, 1), date(1990, 2, 1))]
	print 'GENERATOR DONE'
	# result = p.map(createPanObjectFromInputs, inputsArray)

	for inputs in inputsArray:
		createPanObjectFromInputs(inputs)

	# panObj = createPanObjectFromInputs(inputs, http=True, offline=True)

	print 'Elapsed time: ' + str(time.clock())

if __name__ == '__main__':
	main()