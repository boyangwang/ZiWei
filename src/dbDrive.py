import pymongo
from pymongo import ASCENDING, DESCENDING


class DBDriver(object):

	@staticmethod
	def createIndex():
		client = pymongo.MongoClient(host, port)
		db = client.ziwei

	def __init__(self, host='localhost', port=27017):
		self.client = pymongo.MongoClient(host, port)
		self.db = self.client.ziwei
		self.collection = self.db.zhycw

	def insert(self, doc):
		docId = self.collection.insert(doc)
		return docId