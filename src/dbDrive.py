import pymongo


class DBDriver(object):

	def __init__(self, host='localhost', port=27017):
		self.client = pymongo.MongoClient(host, port)
		self.db = client.ziwei
		self.collection = db.zhycw

	def insert(self, doc):
		docId = self.collection.insert(doc)
		return docId