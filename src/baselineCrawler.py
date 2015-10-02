# -*- coding: utf-8 -*-
import sys
import traceback

import codecs
_open_func_bak = open # Make a back up, just in case
open = codecs.open

import time
from dbDrive import DBDriver
from multiprocessing import Pool
import json
import urllib.request
import socket
from bs4 import BeautifulSoup as BS
from models.Pan import Pan
from models.BaselinePan import BaselinePan
from models.BenMingPan import BenMingPan
from models.DaXianPan import DaXianPan 
from models.LiuNianPan import LiuNianPan

from datetime import date
from datetime import datetime
from dateutil.rrule import rrule, DAILY
import logging
import re

def crawlResponseWithInputs(inputs):
	url = 'http://www.zhycw.com/pp/zw.aspx'
	form_data = inputs
	form_data['submit'] = '%E5%BC%80%E5%A7%8B%E6%8E%92%E7%9B%98',
	form_data_encoded = urllib.parse.urlencode(form_data)
	res = urllib.request.urlopen(url, form_data_encoded.encode('utf-8'))
	res = res.read()
	return res


def createPanObjectFromInputs(inputs, http=True, offline=False):
	page = ''
	try:
		name = Pan.getName(inputs)
		logging.info('START: '+ name)
		
		if (not offline): 
			driver = DBDriver(host='localhost')
		
			results = driver.collection.find({
				'name': name
			})

			# logging.info('LEN: ', results.limit(1).count())


			if (results.limit(1).count() >= 1):
				logging.info('EXIST: '+name)
				return
			# 	if (not isInvalid(results)):
			# 		logging.info('EXIST and VALID: ', name)
			# 		return
			# 	else:
			# 		logging.info('INVALID! redo...')
			# 		driver.collection.remove({
			# 			'name': name
			# 		})


		if (http):	
			page = crawlResponseWithInputs(inputs)
		else:
			page = open('sample-response.html', 'r').read()

		panObj = BaselinePan(inputs, page, logging);


		panObj.serializeToFile()

		mingSiHua = panObj.page.find_all(text=re.compile(u'├─────────┤'))
		logging.debug('mingsihua: ' + str(len(mingSiHua)))

		logging.info('DONE: '+ name)
		return panObj
	except:
		logging.exception('magic?');
		raise
	# 	logging.info('ERROR: '+Pan.getName(inputs))
	# 	logging.info(str(sys.exc_info()[0]) + '\n' + str(e.__doc__) + '\n' + str(e))
	# 	errlog = open('data/errlog-' + Pan.getName(inputs), 'w')
	# 	errlog.write(str(sys.exc_info()[0]) + '\n' + str(e.__doc__) + '\n' + str(e))
	# 	# traceback.print_tb(sys.exc_info()[3], None, errlog)
	# 	traceback.print_exc(None, errlog)
	# 	errlog.write(page)
	# 	return None

def main():
	inputs = {
		'y':2010,
		'm':12,
		'd':31,
		'h':12,
		'min':0,
		'sex':1,
		'mode':1,
	}

	log_file_path = 'crawler-{datetime.year}-{datetime.month}-{datetime.day}-{datetime.hour}-{datetime.minute}-{datetime.second}-starting-{starting[y]}-{starting[m]}-{starting[d]}.log'.format(datetime=datetime.now(), starting=inputs)
	logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(log_file_path, 'w', 'utf-8')])
	
	logging.info('IN MAIN')


	time.clock()

	panObj = createPanObjectFromInputs(inputs, http=True, offline=True)
	logging.info(panObj)
	logging.info('Elapsed time: ' + str(time.clock()))

if __name__ == '__main__':
	main()
