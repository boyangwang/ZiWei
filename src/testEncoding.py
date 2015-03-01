import json
myString = u'中文'
myList = [myString]
myListJson = json.dumps(myList)
myLoadedList = json.loads(myListJson)
print myLoadedList