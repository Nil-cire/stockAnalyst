import pymongo

# connection settings
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
mydb = myclient["test01"]
mycol = mydb["col001"]

# CRUD data

customData = {}

blankFilter = {}

queryFilter = {"_id" : 6.0}
updateDoc = {"$set": {"info.sibling": [1.0, 2.0, 3.0]}}
updateList = {"$push": {"info.sibling": {"$each": [8.0, 9.0]}}}
removeList = {"$pull": {"info.sibling": {"$in" : [1.0, 2.0]}}}
insertDoc = {"_id" : 6.0, "name" : "6", "info" : { "age" : 6.0, "nation": "tw"}}
deleteFilter = {"_id" : 6.0}


# CRUD functions
def insertData(data):
    try:
        mycol.insert_one(data)
        print("success to insertData")
    except Exception as e:
        print("fail to insertData")
        print(e)


def querySingleData(queryFilter):
    print(mycol.find_one(queryFilter))


def queryData(queryFilter):
    for data in list(mycol.find(queryFilter)):
        print(data)


def updateData(queryFilter, updateDoc):
    mycol.update_one(queryFilter, updateDoc)
    queryData(blankFilter)


def deleteData(deleteFilter):
    try:
        mycol.delete_one(deleteFilter)
        print("success to delete")
    except Exception as e:
        print("fail to delete")
        print(e)


# execution
if __name__ == "__main__":
    # insertData(insertDoc)
    updateData(queryFilter, removeList)
    # querySingleData(queryFilter)
    # deleteData(deleteFilter)
    # queryData(customData)