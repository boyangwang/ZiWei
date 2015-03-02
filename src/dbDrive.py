import pymongo


class DBDriver(object):

	def __init__(self, host, port):
		self.client = pymongo.MongoClient(host, port)
		self.db = client.ziwei
		self.collection = db.zhycw

	def insert(self, doc):
		docId = self.collection.insert(doc)
		return docId